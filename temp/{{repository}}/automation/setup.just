# Always run after the creation of a new project, syncs venv en installs pre-commit
[group('setup')]
setup:setup-project setup-hooks

# Create or sync venv and install or update all dependencies
[group('setup')]
setup-project:
    uv sync --all-groups

# Install git hook for commits
[group('setup')]
setup-hooks:
    uv run pre-commit install --hook-type=commit-msg
    uv run pre-commit install --hook-type=pre-commit

[group('setup')]
setup-hooks-clean:
    uv run pre-commit uninstall
