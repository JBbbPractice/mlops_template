# Define behavior when full group is executed
[group('quality')]
quality: quality-code quality-type quality-format quality-security quality-coverage

# Run Ruff to check code quality and find issues
[group('quality')]
quality-code:
    {% raw %}uv run ruff check {{SOURCES}} {{TESTS}}{% endraw %}

# Run Ruff to check code formatting and find issues
[group('quality')]
quality-format:
    {% raw %}uv run ruff format --check {{SOURCES}} {{TESTS}}{% endraw %}

# Use MyPy to statically check code typing
[group('quality')]
quality-type:
    {% raw %}uv run mypy {{SOURCES}} {{TESTS}}{% endraw %}

# Run Bandit to find vulnerabilities in code
[group('quality')]
quality-security:
    {% raw %}uv run bandit --recursive --configfile=pyproject.toml {{SOURCES}}{% endraw %}

# Use Pytest to execute component tests (requires test scripts)
[group('quality')]
quality-test numprocesses="auto":
    {% raw %}uv run pytest --numprocesses={{numprocesses}} {{TESTS}}{% endraw %}

# Check the coverage of the component tests
[group('quality')]
quality-coverage numprocesses="auto" cov_fail_under="80":
    {% raw %}uv run pytest --numprocesses={{numprocesses}} --cov={{SOURCES}} --cov-fail-under={{cov_fail_under}} {{TESTS}}{% endraw %}

# Format imports to adhere to style rules (Important - this command might change current code)
[group('quality')]
quality-importformat:
    {% raw %}uv run ruff check --select=I --fix {{SOURCES}} {{TESTS}}{% endraw %}

# Format code to adhere to ruff pep rules (Important - this command might change current code)
[group('quality')]
quality-codeformat:
    {% raw %}uv run ruff format {{SOURCES}} {{TESTS}}{% endraw %}
