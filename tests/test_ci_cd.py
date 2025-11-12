# ABOUTME: Tests for validating GitLab CI/CD configuration in generated projects.
# ABOUTME: Verifies pipeline structure, stages, rules, and artifact configuration.

import re

import pytest
import yaml

from tests.fixtures.project_generation import GeneratedProject


@pytest.mark.fast
def test_gitlab_ci_is_valid_yaml(default_project: GeneratedProject):
    """Verify that .gitlab-ci.yml is valid YAML syntax."""
    ci_content = default_project.read_file(".gitlab-ci.yml")

    try:
        ci_config = yaml.safe_load(ci_content)
    except yaml.YAMLError as e:
        pytest.fail(f".gitlab-ci.yml contains invalid YAML syntax: {e}")

    assert ci_config is not None, ".gitlab-ci.yml should not be empty"


@pytest.mark.fast
def test_gitlab_ci_has_correct_stages(default_project: GeneratedProject):
    """Verify that pipeline defines the correct stages in order."""
    ci_content = default_project.read_file(".gitlab-ci.yml")
    ci_config = yaml.safe_load(ci_content)

    expected_stages = [
        "tests-coverage",
        "linting-formatting",
        "type-checking",
        "security",
    ]

    assert "stages" in ci_config, ".gitlab-ci.yml should define stages"
    assert ci_config["stages"] == expected_stages, (
        f"Stages should be {expected_stages}, got {ci_config['stages']}"
    )


@pytest.mark.fast
def test_gitlab_ci_uses_correct_docker_image(default_project: GeneratedProject):
    """Verify that pipeline uses the correct Docker image with Python version."""
    ci_content = default_project.read_file(".gitlab-ci.yml")
    ci_config = yaml.safe_load(ci_content)

    # Check default image
    assert "default" in ci_config, ".gitlab-ci.yml should define default configuration"
    assert "image" in ci_config["default"], "Default should specify Docker image"

    expected_image = "ghcr.io/astral-sh/uv:python3.13-bookworm"
    assert ci_config["default"]["image"] == expected_image, (
        f"Docker image should be {expected_image}, got {ci_config['default']['image']}"
    )


@pytest.mark.fast
def test_gitlab_ci_python_version_substitution(generated_project):
    """Verify that Python version template variable is correctly substituted."""
    project = generated_project(python_version="3.12")
    ci_content = project.read_file(".gitlab-ci.yml")
    ci_config = yaml.safe_load(ci_content)

    # Should use Python 3.12 in the image
    expected_image = "ghcr.io/astral-sh/uv:python3.12-bookworm"
    assert ci_config["default"]["image"] == expected_image, (
        f"Docker image should use python_version variable: {expected_image}"
    )


@pytest.mark.fast
def test_gitlab_ci_has_workflow_rules(default_project: GeneratedProject):
    """Verify that pipeline has correct workflow rules for when it runs."""
    ci_content = default_project.read_file(".gitlab-ci.yml")
    ci_config = yaml.safe_load(ci_content)

    assert "workflow" in ci_config, ".gitlab-ci.yml should define workflow rules"
    assert "rules" in ci_config["workflow"], "Workflow should define rules"

    rules = ci_config["workflow"]["rules"]
    assert len(rules) == 3, "Should have 3 workflow rules (MR, main, development)"

    # Check for merge request rule
    mr_rule = next((r for r in rules if "merge_request_event" in str(r)), None)
    assert mr_rule is not None, "Should have rule for merge requests"

    # Check for main branch rule
    main_rule = next((r for r in rules if r.get("if", "").find('"main"') != -1), None)
    assert main_rule is not None, "Should have rule for main branch"

    # Check for development branch rule
    dev_rule = next((r for r in rules if r.get("if", "").find('"development"') != -1), None)
    assert dev_rule is not None, "Should have rule for development branch"


@pytest.mark.fast
def test_gitlab_ci_has_all_jobs(default_project: GeneratedProject):
    """Verify that all required pipeline jobs are defined."""
    ci_content = default_project.read_file(".gitlab-ci.yml")
    ci_config = yaml.safe_load(ci_content)

    expected_jobs = [
        "tests-coverage",
        "linting-formatting",
        "type-checking",
        "security",
    ]

    for job_name in expected_jobs:
        assert job_name in ci_config, f"Job {job_name} should be defined"


@pytest.mark.fast
def test_gitlab_ci_jobs_use_correct_stages(default_project: GeneratedProject):
    """Verify that each job is assigned to the correct stage."""
    ci_content = default_project.read_file(".gitlab-ci.yml")
    ci_config = yaml.safe_load(ci_content)

    job_stage_mapping = {
        "tests-coverage": "tests-coverage",
        "linting-formatting": "linting-formatting",
        "type-checking": "type-checking",
        "security": "security",
    }

    for job_name, expected_stage in job_stage_mapping.items():
        assert "stage" in ci_config[job_name], f"Job {job_name} should specify a stage"
        assert ci_config[job_name]["stage"] == expected_stage, (
            f"Job {job_name} should be in stage {expected_stage}"
        )


@pytest.mark.fast
def test_gitlab_ci_jobs_have_sequential_dependencies(default_project: GeneratedProject):
    """Verify that jobs run sequentially with proper needs dependencies."""
    ci_content = default_project.read_file(".gitlab-ci.yml")
    ci_config = yaml.safe_load(ci_content)

    # First job should have no dependencies
    assert "needs" not in ci_config["tests-coverage"], (
        "First job (tests-coverage) should not have needs dependency"
    )

    # Second job depends on first
    assert "needs" in ci_config["linting-formatting"], (
        "linting-formatting should have needs dependency"
    )
    assert ci_config["linting-formatting"]["needs"] == ["tests-coverage"]

    # Third job depends on second
    assert "needs" in ci_config["type-checking"], (
        "type-checking should have needs dependency"
    )
    assert ci_config["type-checking"]["needs"] == ["linting-formatting"]

    # Fourth job depends on third
    assert "needs" in ci_config["security"], (
        "security should have needs dependency"
    )
    assert ci_config["security"]["needs"] == ["type-checking"]


@pytest.mark.fast
def test_gitlab_ci_jobs_run_quality_commands(default_project: GeneratedProject):
    """Verify that jobs execute the correct just quality commands."""
    ci_content = default_project.read_file(".gitlab-ci.yml")
    ci_config = yaml.safe_load(ci_content)

    job_commands = {
        "tests-coverage": ["just quality-test", "just quality-coverage"],
        "linting-formatting": ["just quality-code", "just quality-format"],
        "type-checking": ["just quality-type"],
        "security": ["just quality-security", "just quality-secrets"],
    }

    for job_name, expected_commands in job_commands.items():
        script = ci_config[job_name].get("script", [])

        # Find the actual quality commands (skip uv sync)
        quality_commands = [cmd for cmd in script if cmd.startswith("just quality-")]

        assert len(quality_commands) == len(expected_commands), (
            f"Job {job_name} should run {len(expected_commands)} quality commands"
        )

        for expected_cmd in expected_commands:
            assert expected_cmd in script, (
                f"Job {job_name} should include command '{expected_cmd}'"
            )


@pytest.mark.fast
def test_gitlab_ci_jobs_install_dependencies(default_project: GeneratedProject):
    """Verify that all jobs install dependencies using uv sync."""
    ci_content = default_project.read_file(".gitlab-ci.yml")
    ci_config = yaml.safe_load(ci_content)

    jobs = ["tests-coverage", "linting-formatting", "type-checking", "security"]

    for job_name in jobs:
        script = ci_config[job_name].get("script", [])

        # Should have uv sync command
        has_uv_sync = any("uv sync" in cmd for cmd in script)
        assert has_uv_sync, f"Job {job_name} should install dependencies with 'uv sync'"


@pytest.mark.fast
def test_gitlab_ci_jobs_save_artifacts(default_project: GeneratedProject):
    """Verify that jobs save appropriate artifacts."""
    ci_content = default_project.read_file(".gitlab-ci.yml")
    ci_config = yaml.safe_load(ci_content)

    # Tests-coverage job should save test reports
    assert "artifacts" in ci_config["tests-coverage"], (
        "tests-coverage job should define artifacts"
    )

    artifacts = ci_config["tests-coverage"]["artifacts"]
    assert "when" in artifacts, "Artifacts should specify 'when' condition"
    assert artifacts["when"] == "always", "Artifacts should be saved always (even on failure)"

    assert "reports" in artifacts, "Artifacts should include reports"
    assert "junit" in artifacts["reports"], "Should save JUnit test reports"


@pytest.mark.fast
def test_gitlab_ci_no_template_placeholders(default_project: GeneratedProject):
    """Verify that no Jinja2 template placeholders remain in .gitlab-ci.yml."""
    ci_content = default_project.read_file(".gitlab-ci.yml")

    # Pattern to match Jinja2 template variables
    placeholder_pattern = re.compile(r"\{\{[^}]+\}\}")
    matches = placeholder_pattern.findall(ci_content)

    assert not matches, (
        f".gitlab-ci.yml contains unsubstituted template placeholders: {matches}"
    )
