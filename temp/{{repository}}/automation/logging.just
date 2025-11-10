# Define behavior when full group is executed
[group('logging')]
logging: logging-code

# Run Ruff to check code logging and find issues
[group('logging')]
logging-code:
    uv run python -m microlog "microlog-test-application" src/application.py
