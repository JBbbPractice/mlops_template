# Define default command when user types just in terminal
default:
    @just --list

# Install the project defined in pyproject.toml
install:
    uv sync --all-groups

# Setup the pre-commit hooks
hooks:
    uv run pre-commit install --hook-type=commit-msg

# Run the project component tests
test:
    uv run pytest tests/

# Add all changes to staging and commit with proper formatting
commit:
    git add .
    uv run cz commit
