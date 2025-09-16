# Define default command when user types just in terminal
default:
    @just --list

# Install the project defined in pyproject.toml
install:
    uv sync --all-groups

# Setup the pre-commit hooks
hooks:
    uv run pre-commit install --hook-type=pre-commit
    uv run pre-commit install --hook-type=commit-msg

# Run the project component tests
test:
    uv run pytest tests/

# Add all changes to staging and commit with proper formatting
add:
    git add .

commitregular:
    git commit

commit:
    uv run cz commit

message:
    git config commit.template .gitmessage

# Create and push a new git branch
new-branch:
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
