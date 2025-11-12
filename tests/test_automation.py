# ABOUTME: Tests for validating full automation suite in generated projects.
# ABOUTME: Runs Just commands (package, docker, document) to ensure complete workflow works.

import pytest

from tests.fixtures.project_generation import GeneratedProject


@pytest.mark.automation
@pytest.mark.slow
def test_test_command(default_project: GeneratedProject):
    """Verify that just test runs successfully."""
    default_project.run("just setup")

    result = default_project.run("just test", check=False)

    assert result.returncode == 0, (
        f"just test failed with exit code {result.returncode}\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )


@pytest.mark.automation
@pytest.mark.slow
def test_package_build(default_project: GeneratedProject):
    """Verify that package building works and creates a wheel."""
    default_project.run("just setup")

    result = default_project.run("just package-build", check=False)

    assert result.returncode == 0, (
        f"just package-build failed with exit code {result.returncode}\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )

    # Verify wheel was created
    assert default_project.file_exists("dist"), "dist directory should exist"

    # Check for .whl file in dist/
    dist_files = list((default_project.path / "dist").glob("*.whl"))
    assert len(dist_files) > 0, "At least one .whl file should be created in dist/"


@pytest.mark.automation
@pytest.mark.slow
def test_docker_build(default_project: GeneratedProject):
    """Verify that Docker image builds successfully."""
    default_project.run("just setup")

    result = default_project.run("just docker-build", check=False)

    assert result.returncode == 0, (
        f"just docker-build failed with exit code {result.returncode}\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )


@pytest.mark.automation
@pytest.mark.slow
def test_document_generation(default_project: GeneratedProject):
    """Verify that documentation generation works."""
    default_project.run("just setup")

    result = default_project.run("just document", check=False)

    assert result.returncode == 0, (
        f"just document failed with exit code {result.returncode}\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )

    # Verify docs were created
    assert default_project.file_exists("docs"), "docs directory should exist after generation"
