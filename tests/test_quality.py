# ABOUTME: Tests for validating quality gates in generated projects.
# ABOUTME: Runs quality commands (ruff, pyrefly, bandit, etc.) on fresh projects.

import pytest

from tests.fixtures.project_generation import GeneratedProject


@pytest.mark.quality
def test_setup_succeeds(default_project: GeneratedProject):
    """Verify that just setup runs successfully in a generated project."""
    result = default_project.run("just setup", check=False)

    assert result.returncode == 0, (
        f"just setup failed with exit code {result.returncode}\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )


@pytest.mark.quality
def test_quality_code_passes(default_project: GeneratedProject):
    """Verify that ruff linting passes in a generated project."""
    # First run setup to ensure environment is ready
    default_project.run("just setup")

    # Run ruff linting
    result = default_project.run("just quality-code", check=False)

    assert result.returncode == 0, (
        f"just quality-code failed with exit code {result.returncode}\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )


@pytest.mark.quality
def test_quality_format_passes(default_project: GeneratedProject):
    """Verify that format checking passes in a generated project."""
    default_project.run("just setup")

    result = default_project.run("just quality-format", check=False)

    assert result.returncode == 0, (
        f"just quality-format failed with exit code {result.returncode}\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )


@pytest.mark.quality
def test_quality_type_passes(default_project: GeneratedProject):
    """Verify that type checking passes in a generated project."""
    default_project.run("just setup")

    result = default_project.run("just quality-type", check=False)

    assert result.returncode == 0, (
        f"just quality-type failed with exit code {result.returncode}\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )


@pytest.mark.quality
def test_quality_security_passes(default_project: GeneratedProject):
    """Verify that security scanning passes in a generated project."""
    default_project.run("just setup")

    result = default_project.run("just quality-security", check=False)

    assert result.returncode == 0, (
        f"just quality-security failed with exit code {result.returncode}\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )


@pytest.mark.quality
def test_quality_secrets_passes(default_project: GeneratedProject):
    """Verify that secret detection passes in a generated project."""
    default_project.run("just setup")

    result = default_project.run("just quality-secrets", check=False)

    assert result.returncode == 0, (
        f"just quality-secrets failed with exit code {result.returncode}\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )


@pytest.mark.quality
@pytest.mark.slow
def test_all_quality_gates(default_project: GeneratedProject):
    """Verify that all quality gates pass together."""
    default_project.run("just setup")

    result = default_project.run("just quality", check=False)

    assert result.returncode == 0, (
        f"just quality failed with exit code {result.returncode}\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )
