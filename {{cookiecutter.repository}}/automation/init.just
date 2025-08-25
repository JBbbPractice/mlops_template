# Run commands needed to initialize repo
[group('init')]
init: init-project init-hook

# Create venv,
[group('init')]
init-project:
    uv sync --all-groups

# Install git hook for commits
[group('install')]
install-hooks:
    uv run pre-commit install --hook-type=commit-msg
