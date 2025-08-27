# Run when version/tag needs bumped after changes
[group('version')]
version-bump:
    uv run cz bump

# Start commit process for staged changes
[group('version')]
version-commit:
    uv run cz commit

# Undo last commit not yet pushed to origin
[group('version')]
version-undo-commit:
    git reset HEAD~

# Stage all current workspace changes and start commit process
[group('version')]
version-stage-commit:
    git add .
    uv run cz commit

# Return commit information
[group('version')]
version-info:
    uv run cz info

# Create and push a new git branch
[group('version')]
version-new-branch:
    #!/usr/bin/env bash
    set -euo pipefail

    echo
    echo "Creating a new git branch based on current branch..."
    echo
    echo "Branch name rules:"
    echo "  - Use lowercase letters, numbers, hyphens, and forward slashes"
    echo "  - Start with a letter"
    echo "  - No spaces or special characters except hyphens and slashes"
    echo
    echo "Common prefixes:"
    echo "  • feature/    - For new features or major changes"
    echo "  • bugfix/     - For fixing bugs"
    echo "  • hotfix/     - For urgent fixes in production"
    echo "  • release/    - For preparing a new release"
    echo "  • improvement/ - For enhancements or optimizations"
    echo "  • experiment/ - For trying out new ideas"
    echo
    echo "Examples: feature/user-login, bugfix/header-layout, hotfix/security-patch"
    echo

    read -p "Enter branch name: " branch_name

    # Validate branch name (allow forward slashes for prefixes)
    if [[ ! "$branch_name" =~ ^[a-z][a-z0-9/-]*$ ]]; then
        echo "❌ Invalid branch name. Please follow the naming rules."
        exit 1
    fi

    echo "Creating branch '$branch_name'..."
    git checkout -b "$branch_name"
    echo
    echo "Pushing branch to origin..."
    git push -u origin "$branch_name"
    echo
    echo "✅ Branch '$branch_name' created and pushed successfully!"
