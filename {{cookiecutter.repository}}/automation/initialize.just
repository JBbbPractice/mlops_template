# Always run after the creation of a new project, syncs venv en installs pre-commit
[group('initialize')]
initialize:initialize-project initialize-hooks

# Create venv and install all dependencies (better to run group)
[group('initialize')]
initialize-project:
    uv sync --all-groups

# Install git hook for commits
[group('initialize')]
initialize-hooks:
    uv run pre-commit install --hook-type=commit-msg
    uv run pre-commit install --hook-type=pre-commit
