# ABOUTME: Pytest configuration and shared fixtures for template testing.
# ABOUTME: Contains fixtures for generating test projects and common test utilities.

import subprocess
import tempfile
from pathlib import Path
from typing import Any, Callable

import pytest

from tests.fixtures.project_generation import (
    GeneratedProject,
    cleanup_project,
    generate_project,
)


def _print_project_diagnostics(project: GeneratedProject) -> None:
    """Print diagnostic information about a generated project on test failure.

    Args:
        project: The generated project to diagnose
    """
    print(f"\n{'='*80}")
    print(f"GENERATED PROJECT PRESERVED FOR DEBUGGING")
    print(f"{'='*80}")
    print(f"\nProject location: {project.path}")
    print(f"\nProject structure:")

    # Use find command to show directory tree
    result = subprocess.run(
        ["find", str(project.path), "-maxdepth", "3", "-type", "f"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode == 0:
        files = result.stdout.strip().split("\n")
        for file_path in sorted(files):
            # Make path relative to project root for readability
            rel_path = Path(file_path).relative_to(project.path)
            print(f"  {rel_path}")
    else:
        print("  (Could not generate file tree)")

    print(f"\n{'='*80}\n")


@pytest.fixture
def template_path() -> Path:
    """Path to the template root directory (where copier.yml is located)."""
    return Path(__file__).parent.parent


@pytest.fixture
def generated_project(
    template_path: Path,
    request: pytest.FixtureRequest,
) -> Callable[..., GeneratedProject]:
    """Factory fixture for generating test projects with custom parameters.

    Returns a function that accepts copier parameters and returns a GeneratedProject.
    The generated project is automatically cleaned up after the test unless it fails.

    Example:
        def test_something(generated_project):
            project = generated_project(name="my-app", python_version="3.13")
            assert project.file_exists("pyproject.toml")
    """
    projects: list[GeneratedProject] = []

    def _generate(**copier_data: Any) -> GeneratedProject:
        # Create temporary directory for the project
        temp_dir = Path(tempfile.mkdtemp(prefix="test-project-"))

        # Set default copier data
        defaults = {
            "name": "test-project",
            "version": "0.1.0",
            "author": "Test Author",
            "description": "Test project",
            "python_version": "3.13",
        }
        defaults.update(copier_data)

        # Generate project
        project = generate_project(template_path, temp_dir, **defaults)
        projects.append(project)
        return project

    yield _generate

    # Cleanup logic with failure preservation
    test_failed = request.session.testsfailed > 0 if hasattr(request.session, "testsfailed") else False

    for project in projects:
        if test_failed:
            # Preserve project on failure and generate diagnostics
            _print_project_diagnostics(project)
        else:
            # Clean up on success
            cleanup_project(project)


@pytest.fixture
def default_project(generated_project: Callable[..., GeneratedProject]) -> GeneratedProject:
    """Convenience fixture that generates a project with default parameters.

    Example:
        def test_structure(default_project):
            assert default_project.file_exists("pyproject.toml")
    """
    return generated_project()
