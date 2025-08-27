# Run commands needed to initialize repo
[group('init')]
init: init-project init-hooks

# Create venv and install all dependencies (better to run group)
[group('init')]
init-project:    
    uv sync --all-groups

# Install git hook for commits
[group('init')]
init-hooks:
    uv run pre-commit install --hook-type=commit-msg
