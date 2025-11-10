# Define behavior when full group is executed
[group('quality')]
quality: quality-code quality-type quality-format quality-security quality-test quality-coverage

# Run Ruff to check code quality and find issues
[group('quality')]
quality-code:
    uv run ruff check {{SOURCES}} {{TESTS}}

# Run Ruff to check code formatting and find issues
[group('quality')]
quality-format:
    uv run ruff format --check {{SOURCES}} {{TESTS}}

# Pyrefly to perform static type checking
[group('quality')]
quality-type:
    uv run pyrefly check {{SOURCES}} {{TESTS}} --summarize-errors

# Run Bandit to find vulnerabilities in code
[group('quality')]
quality-security:
    uv run bandit --recursive --configfile=pyproject.toml {{SOURCES}}

# Run Trufflehog to find secrets
[group('quality')]
quality-secrets:
    uv run trufflehog filesystem .

# Use Pytest to execute component tests (requires test scripts)
[group('quality')]
quality-test:
    uv run pytest {{TESTS}}

# Check the coverage of the component tests
[group('quality')]
quality-coverage:
    uv run coverage run -m pytest {{TESTS}} && uv run coverage report -m

# Format imports to adhere to style rules (Important - this command might change current code)
[group('quality')]
quality-importformat:
    uv run ruff check --select=I --fix {{SOURCES}} {{TESTS}}

# Format code to adhere to ruff pep rules (Important - this command might change current code)
[group('quality')]
quality-codeformat:
    uv run ruff format {{SOURCES}} {{TESTS}}
