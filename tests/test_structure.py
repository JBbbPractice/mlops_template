# ABOUTME: Tests for validating generated project structure and file existence.
# ABOUTME: Fast tests that verify template generates correct directory layout and files.

import re

import pytest

from tests.fixtures.project_generation import GeneratedProject


@pytest.mark.fast
def test_directory_structure_exists(default_project: GeneratedProject):
    """Verify that all key directories are created in the generated project."""
    expected_dirs = [
        "src",
        "src/test_project",
        "src/test_project/domain",
        "src/test_project/io",
        "src/test_project/workflows",
        "src/test_project/utils",
        "tests",
        "automation",
        "config",
        "docs",
        "experiments",
        "notebooks",
    ]

    for directory in expected_dirs:
        assert default_project.file_exists(directory), f"Directory {directory} should exist"


@pytest.mark.fast
def test_core_files_exist(default_project: GeneratedProject):
    """Verify that core project files are created."""
    expected_files = [
        "pyproject.toml",
        "justfile",
        "Dockerfile",
        "README.md",
        ".gitignore",
        ".pre-commit-config.yaml",
        ".env.example",
        ".gitlab-ci.yml",
    ]

    for file_path in expected_files:
        assert default_project.file_exists(file_path), f"File {file_path} should exist"


@pytest.mark.fast
def test_source_structure(default_project: GeneratedProject):
    """Verify that the source code structure is properly created."""
    expected_source_files = [
        "src/test_project/__init__.py",
        "src/test_project/__main__.py",
        "src/test_project/application.py",
        "src/test_project/domain/__init__.py",
        "src/test_project/io/__init__.py",
        "src/test_project/workflows/__init__.py",
        "src/test_project/utils/__init__.py",
    ]

    for file_path in expected_source_files:
        assert default_project.file_exists(file_path), f"Source file {file_path} should exist"


@pytest.mark.fast
def test_automation_files_exist(default_project: GeneratedProject):
    """Verify that automation files in the automation/ directory are created."""
    expected_automation_files = [
        "automation/setup.just",
        "automation/quality.just",
        "automation/package.just",
        "automation/docker.just",
        "automation/version.just",
        "automation/document.just",
        "automation/logging.just",
        "automation/remove.just",
    ]

    for file_path in expected_automation_files:
        assert default_project.file_exists(file_path), f"Automation file {file_path} should exist"


@pytest.mark.fast
def test_config_files_exist(default_project: GeneratedProject):
    """Verify that configuration files are created."""
    expected_config_files = [
        "config/dev.yml",
        "config/prod.yml",
    ]

    for file_path in expected_config_files:
        assert default_project.file_exists(file_path), f"Config file {file_path} should exist"


@pytest.mark.fast
def test_no_template_placeholders_in_core_files(default_project: GeneratedProject):
    """Verify that template placeholders are properly substituted in core files."""
    # Pattern to match Jinja2 template variables
    placeholder_pattern = re.compile(r"\{\{[^}]+\}\}")

    files_to_check = [
        "pyproject.toml",
        "justfile",
        "Dockerfile",
        "README.md",
        "src/test_project/__init__.py",
        "src/test_project/__main__.py",
        "src/test_project/application.py",
    ]

    for file_path in files_to_check:
        if default_project.file_exists(file_path):
            content = default_project.read_file(file_path)
            matches = placeholder_pattern.findall(content)
            assert not matches, (
                f"File {file_path} contains unsubstituted template placeholders: {matches}"
            )


@pytest.mark.fast
def test_package_name_substitution(default_project: GeneratedProject):
    """Verify that the package name is correctly substituted throughout the project."""
    # Check that the source directory uses the correct package name
    assert default_project.file_exists("src/test_project"), (
        "Source directory should use substituted package name 'test_project'"
    )

    # Verify no template placeholders remain in __init__.py
    init_content = default_project.read_file("src/test_project/__init__.py")
    placeholder_pattern = re.compile(r"\{\{[^}]+\}\}")
    assert not placeholder_pattern.search(init_content), (
        "Package __init__.py should not contain template placeholders"
    )


@pytest.mark.fast
def test_project_name_in_pyproject(default_project: GeneratedProject):
    """Verify that project metadata is correctly substituted in pyproject.toml."""
    pyproject_content = default_project.read_file("pyproject.toml")

    # Check for expected substitutions
    assert 'name = "test-project"' in pyproject_content, (
        "pyproject.toml should contain correct project name"
    )
    assert 'version = "0.1.0"' in pyproject_content, (
        "pyproject.toml should contain correct version"
    )
    assert 'description = "Test project"' in pyproject_content, (
        "pyproject.toml should contain correct description"
    )
