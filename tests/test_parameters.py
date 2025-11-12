# ABOUTME: Tests for validating template with different parameter combinations.
# ABOUTME: Parametrized tests covering various configurations and edge cases.

import re
from pathlib import Path

import pytest
import yaml

from tests.fixtures.project_generation import GeneratedProject


def load_parameter_matrix():
    """Load parameter matrix from YAML file."""
    matrix_file = Path(__file__).parent / "data" / "parameter_matrix.yml"
    with open(matrix_file) as f:
        return yaml.safe_load(f)


PARAMETER_MATRIX = load_parameter_matrix()


@pytest.mark.parametrized
@pytest.mark.parametrize("params", PARAMETER_MATRIX["quick"])
def test_quick_parameters(generated_project, params):
    """Test template generation with quick parameter set."""
    project = generated_project(**params)

    # Basic structure validation
    assert project.file_exists("pyproject.toml")
    assert project.file_exists("justfile")
    assert project.file_exists("Dockerfile")

    # Verify no template placeholders
    pyproject_content = project.read_file("pyproject.toml")
    placeholder_pattern = re.compile(r"\{\{[^}]+\}\}")
    assert not placeholder_pattern.search(pyproject_content), (
        "pyproject.toml should not contain template placeholders"
    )


@pytest.mark.parametrized
@pytest.mark.parametrize("params", PARAMETER_MATRIX["standard"])
def test_standard_parameters(generated_project, params):
    """Test template generation with standard parameter variations."""
    project = generated_project(**params)

    # Structure validation
    assert project.file_exists("pyproject.toml")
    assert project.file_exists("src")

    # Verify parameter substitution in pyproject.toml
    pyproject_content = project.read_file("pyproject.toml")
    repository_name = params.get("repository", params["name"].lower().replace(" ", "-"))

    assert f'name = "{repository_name}"' in pyproject_content
    assert f'version = "{params["version"]}"' in pyproject_content
    assert f'description = "{params["description"]}"' in pyproject_content

    # Verify Python version in pyproject.toml
    python_version = params["python_version"]
    assert f">={python_version}" in pyproject_content


@pytest.mark.parametrized
@pytest.mark.parametrize("params", PARAMETER_MATRIX["edge_cases"])
def test_edge_case_parameters(generated_project, params):
    """Test template generation with edge case parameters."""
    project = generated_project(**params)

    # Basic validation
    assert project.file_exists("pyproject.toml")
    assert project.file_exists("justfile")

    # Verify package name is properly generated
    repository_name = params.get("repository", params["name"].lower().replace(" ", "-"))
    package_name = params.get("package", repository_name.replace("-", "_"))

    assert project.file_exists(f"src/{package_name}")

    # Verify no template placeholders remain
    core_files = ["pyproject.toml", "README.md", "Dockerfile"]
    placeholder_pattern = re.compile(r"\{\{[^}]+\}\}")

    for file_path in core_files:
        if project.file_exists(file_path):
            content = project.read_file(file_path)
            assert not placeholder_pattern.search(content), (
                f"{file_path} should not contain template placeholders"
            )
