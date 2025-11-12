# ABOUTME: Fixtures and utilities for generating test projects with Copier.
# ABOUTME: Handles project generation, cleanup, and provides project interaction API.

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from copier import run_copy


class GeneratedProject:
    """Represents a generated test project with helper methods."""

    def __init__(self, path: Path):
        self.path = path

    def run(self, command: str, check: bool = True) -> subprocess.CompletedProcess:
        """Execute a command in the project directory.

        Args:
            command: Shell command to execute
            check: If True, raise exception on non-zero exit code

        Returns:
            CompletedProcess with stdout, stderr, and returncode
        """
        result = subprocess.run(
            command,
            shell=True,
            cwd=self.path,
            capture_output=True,
            text=True,
            check=check,
        )
        return result

    def file_exists(self, relative_path: str) -> bool:
        """Check if a file exists in the generated project.

        Args:
            relative_path: Path relative to project root

        Returns:
            True if file exists, False otherwise
        """
        return (self.path / relative_path).exists()

    def read_file(self, relative_path: str) -> str:
        """Read file contents from the generated project.

        Args:
            relative_path: Path relative to project root

        Returns:
            File contents as string
        """
        return (self.path / relative_path).read_text()


def generate_project(
    template_path: Path,
    dest_path: Path,
    **copier_data: Any,
) -> GeneratedProject:
    """Generate a project from the template using Copier.

    Args:
        template_path: Path to the template directory
        dest_path: Destination directory for generated project
        **copier_data: Copier template variables (name, version, etc.)

    Returns:
        GeneratedProject instance
    """
    # Calculate the repository name (copier will create a subdirectory with this name)
    # The template defines: repository = "{{ name | lower | replace(' ', '-') }}"
    name = copier_data.get("name", "test-project")
    repository = copier_data.get("repository", name.lower().replace(" ", "-"))

    # Use copier's Python API to generate the project
    run_copy(
        src_path=str(template_path),
        dst_path=str(dest_path),
        data=copier_data,
        defaults=True,
        overwrite=True,
        unsafe=True,  # Allow running in non-interactive mode
    )

    # Copier creates the project in a subdirectory named after the repository
    actual_project_path = dest_path / repository
    return GeneratedProject(actual_project_path)


def cleanup_project(project: GeneratedProject) -> None:
    """Remove a generated project directory.

    Args:
        project: GeneratedProject to clean up
    """
    if project.path.exists():
        shutil.rmtree(project.path)
