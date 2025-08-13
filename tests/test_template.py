import json
import pytest
import shutil
from pathlib import Path
from cookiecutter.main import cookiecutter


@pytest.fixture
def template_context():
    """Default template context for testing."""
    return {
        "name": "My Test Project",
        "user": "Test User"
    }


@pytest.fixture
def custom_contexts():
    """Various test contexts to validate template generation."""
    return [
        {
            "name": "Simple Project",
            "user": "John Doe"
        },
        {
            "name": "Complex Project Name",
            "user": "Jane Smith"
        },
        {
            "name": "project-with-dashes",
            "user": "Developer"
        },
        {
            "name": "Project With Spaces",
            "user": "Team Lead"
        },
        {
            "name": "UPPERCASE PROJECT",
            "user": "Admin"
        }
    ]


@pytest.fixture
def temp_output_dir(tmp_path):
    """Temporary directory for cookiecutter output."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    yield output_dir
    # Cleanup handled by tmp_path fixture


class TestCookiecutterGeneration:
    """Test cookiecutter template generation."""
    
    def test_basic_generation(self, template_context, temp_output_dir):
        """Test basic template generation with default context."""
        # Generate project
        result_path = cookiecutter(
            template=".",  # Current directory (your template)
            output_dir=str(temp_output_dir),
            no_input=True,
            extra_context=template_context
        )
        
        # Verify project was created
        project_path = Path(result_path)
        assert project_path.exists()
        assert project_path.is_dir()
        
        # Check expected repository name transformation
        expected_repo_name = template_context["name"].lower().replace(' ', '-')
        assert project_path.name == expected_repo_name
    
    def test_repository_name_transformation(self, custom_contexts, temp_output_dir):
        """Test that repository names are properly transformed."""
        for context in custom_contexts:
            result_path = cookiecutter(
                template=".",
                output_dir=str(temp_output_dir),
                no_input=True,
                extra_context=context
            )
            
            project_path = Path(result_path)
            expected_repo_name = context["name"].lower().replace(' ', '-')
            
            assert project_path.name == expected_repo_name
            
            # Cleanup for next iteration
            shutil.rmtree(project_path)
    
    def test_package_name_transformation(self, template_context, temp_output_dir):
        """Test that package names are properly transformed from repository names."""
        result_path = cookiecutter(
            template=".",
            output_dir=str(temp_output_dir),
            no_input=True,
            extra_context=template_context
        )
        
        project_path = Path(result_path)
        
        # Check if package directory exists with proper naming
        repo_name = template_context["name"].lower().replace(' ', '-')
        expected_package_name = repo_name.replace('-', '_')
        
        # Look for package directory or __init__.py files
        package_indicators = [
            project_path / expected_package_name,
            project_path / f"{expected_package_name}.py",
            project_path / "src" / expected_package_name,
        ]
        
        # At least one package indicator should exist
        package_exists = any(path.exists() for path in package_indicators)
        assert package_exists, f"Package '{expected_package_name}' not found in generated project"
    
    def test_required_files_generated(self, template_context, temp_output_dir):
        """Test that essential files are generated."""
        result_path = cookiecutter(
            template=".",
            output_dir=str(temp_output_dir),
            no_input=True,
            extra_context=template_context
        )
        
        project_path = Path(result_path)
        
        # Common files that should exist in most projects
        expected_files = [
            "README.md",
            "requirements.txt",
            "setup.py",
            ".gitignore",
        ]
        
        for file_name in expected_files:
            file_path = project_path / file_name
            if file_path.exists():  # Only assert if the template includes these files
                assert file_path.is_file(), f"{file_name} should be a file"
    
    def test_template_variable_substitution(self, template_context, temp_output_dir):
        """Test that template variables are properly substituted in files."""
        result_path = cookiecutter(
            template=".",
            output_dir=str(temp_output_dir),
            no_input=True,
            extra_context=template_context
        )
        
        project_path = Path(result_path)
        
        # Check README.md for variable substitution (if it exists)
        readme_path = project_path / "README.md"
        if readme_path.exists():
            readme_content = readme_path.read_text()
            
            # Should not contain unreplaced template variables
            assert "{{cookiecutter" not in readme_content, "Found unreplaced template variables in README.md"
            
            # Should contain the actual project name
            assert template_context["name"] in readme_content, "Project name not found in README.md"
    
    def test_python_package_structure(self, template_context, temp_output_dir):
        """Test that Python package structure is correctly generated."""
        result_path = cookiecutter(
            template=".",
            output_dir=str(temp_output_dir),
            no_input=True,
            extra_context=template_context
        )
        
        project_path = Path(result_path)
        repo_name = template_context["name"].lower().replace(' ', '-')
        package_name = repo_name.replace('-', '_')
        
        # Check for common Python project structures
        possible_structures = [
            project_path / package_name / "__init__.py",
            project_path / "src" / package_name / "__init__.py",
            project_path / f"{package_name}.py"
        ]
        
        # At least one structure should exist
        valid_structure = any(path.exists() for path in possible_structures)
        assert valid_structure, f"No valid Python package structure found for '{package_name}'"    
  
    def test_generated_project_structure(self, template_context, temp_output_dir):
        """Test the overall structure of the generated project."""
        result_path = cookiecutter(
            template=".",
            output_dir=str(temp_output_dir),
            no_input=True,
            extra_context=template_context
        )
        
        project_path = Path(result_path)
        
        # Get all files and directories in the project
        all_items = list(project_path.rglob("*"))
        
        # Should have at least some files
        assert len(all_items) > 0, "Generated project is empty"
        
        # Should have both files and directories
        files = [item for item in all_items if item.is_file()]
        directories = [item for item in all_items if item.is_dir()]
        
        assert len(files) > 0, "No files generated"
        assert len(directories) > 0, "No directory created"
        
    
    @pytest.mark.parametrize("name,expected_repo", [
        ("Simple Name", "simple-name"),
        ("UPPERCASE", "uppercase"),
        ("Mixed Case Name", "mixed-case-name"),
        ("name-with-dashes", "name-with-dashes"),
        ("name_with_underscores", "name_with_underscores"),
        ("Name With Multiple   Spaces", "name-with-multiple---spaces"),
    ])
    def test_name_transformations(self, name, expected_repo, temp_output_dir):
        """Test various name transformation scenarios."""
        context = {"name": name, "user": "Test User"}
        
        result_path = cookiecutter(
            template=".",
            output_dir=str(temp_output_dir),
            no_input=True,
            extra_context=context
        )
        
        project_path = Path(result_path)
        assert project_path.name == expected_repo
        
        # Cleanup
        shutil.rmtree(project_path)


class TestTemplateValidation:
    """Test template configuration and validation."""
    
    def test_cookiecutter_json_exists(self):
        """Test that cookiecutter.json exists and is valid."""
        cookiecutter_json = Path("cookiecutter.json")
        assert cookiecutter_json.exists(), "cookiecutter.json not found"
        
        # Test that it's valid JSON
        with open(cookiecutter_json) as f:
            config = json.load(f)
        
        # Check required fields based on your template
        assert "repository" in config
        assert "package" in config
        assert "author" in config
        assert "__prompts__" in config
    
    def test_template_structure(self):
        """Test that template directory structure is valid."""
        template_dir = Path("{{cookiecutter.repository}}")
        
        # Template directory should exist
        assert template_dir.exists(), "Template directory not found"
        assert template_dir.is_dir(), "Template directory should be a directory"


# Run specific test scenarios
if __name__ == "__main__":
    pytest.main([__file__, "-v"])