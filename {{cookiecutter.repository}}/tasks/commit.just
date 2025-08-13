# Run when version/tag needs bumped after changes
[group('commit')]
commit-bump:
    uv run cz bump

# Stage all current workspace changes and start commit process
[group('commit')]
commit-files:
    git add .
    uv run cz commit

# Return commit information
[group('commit')]
commit-info:
    uv run cz info
