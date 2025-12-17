# MLOps Template

A comprehensive MLOps template for developing production-ready AI systems with Python, emphasizing software engineering best practices including typing, linting, testing, logging, security, formatting, and debugging.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Features

- 🚀 End-to-end MLOps pipeline template
- 🔧 Pre-configured development environment with VSCode workspace
- 🧪 Testing framework setup
- 📝 Automated code formatting and linting
- 🔒 Security scanning with Trufflehog and Bandit
- 📊 Logging and monitoring foundations
- 🏷️ Semantic versioning with conventional commits
- 🌿 Git workflow with protected branches

## Prerequisites

Before getting started, ensure you have the following tools installed:

### Required Tools

| Tool              | Purpose                    | Installation Link                                                                |
| ----------------- | -------------------------- | -------------------------------------------------------------------------------- |
| **VSCode**        | Primary IDE                | [Download VSCode](https://code.visualstudio.com/Download)                        |
| **uv**            | Python package manager     | [uv Installation Guide](https://docs.astral.sh/uv/getting-started/installation/) |
| **Git with Bash** | Version control & terminal | [Git Downloads](https://git-scm.com/downloads)                                   |
| **Trufflehog**    | Security scanning          | [Trufflehog Repository](https://github.com/trufflesecurity/trufflehog)           |
| **Trivy**         | Security scanning          | [Trivy Repository](https://trivy.dev/docs/latest/)                               |

### Environment Setup

1. **Configure VSCode**: Set Bash as your default terminal
   - Open VSCode → Terminal → Select Default Profile → Choose "Git Bash"
2. **Verify Installation**: Run the following commands to verify your setup:
   ```bash
   uv --version
   git --version
   trufflehog --version
   trivy --version
   ```

> ⚠️ **Important**: This template requires Bash terminal functionality. Windows users must use Git Bash or WSL.

## Detailed Setup

### 1a. Project Generation in current folder

```bash
# Move to the folder where your project folder should be created
cd /path/to/projects

# Create new project from template
uvx copier copy https://github.com/YOUR_USERNAME/TEMPLATE_REPO.git 

# Follow the interactive prompts to configure your project
```

### 1b. Project Generation to folder of your choice

```bash
# Create new project from template
uvx copier copy https://github.com/YOUR_USERNAME/TEMPLATE_REPO.git /path/to/projects/folder

# Follow the interactive prompts to configure your project
# IMPORTANT - When /path/to/projects/folder already contains a folder with the intended repo name, a duplicate folder will be created.
```

### 2. Project Initialization

```bash
# Open the newly created project folder in VSCode
code your-project-name

# Open the VSCode workspace file
# File → Open Workspace from File → select `your-project.code-workspace`
```

### 3. Environment Setup

```bash
# Install dependencies and create virtual environment
uv sync

# VSCode will prompt to use the new Python interpreter - select Yes
# If no prompt appears: Ctrl+Shift+P → "Python: Select Interpreter" → Choose .venv/python
```

### 4. Initialize Version Control

```bash
# Initialize git repository
git init

# Install pre-commit hooks and quality controls (Make sure your local virtual environment is activated!)
just setup

# View available just commands
just
```

### 5. First Commit

```bash
# Create your first commit using semantic versioning
just version

# Follow the interactive prompts:
# - Type: feat
# - Scope: repo
# - Subject: first commit
```

### 5. Remote Repository Setup

1. **Create Remote Repository**:
   - Go to GitLab/GitHub
   - Create new **private** repository
   - ⚠️ **Do not** add README, LICENSE, or .gitignore

2. **Link Remote Repository**:
   ```bash
   # Add remote origin
   git remote add origin https://github.com/YOUR_USERNAME/your-repo.git

   # Push and set upstream
   git push --set-upstream origin main  # or 'master' depending on your setup
   ```

### 6. Branch Protection Setup

```bash
# Create development branch
just version-new-branch
# Enter branch name: development

# The command will:
# - Create branch locally and remotely
# - Set up tracking
# - Check out the new branch
```

**Configure Branch Protection** (GitLab/GitHub):
- Navigate to repository settings
- Set main/master branch as protected
- Require pull/merge requests for changes

## Usage

### Available Just Commands

Run `just` to see all available commands. Common commands include:

- `just setup` - Set up pre-commit hooks and quality controls
- `just version` - Create semantic version commit
- `just version-new-branch` - Create and setup new branch
- `just quality` - Run test, linting, formatting and security checks
- `just docker` - Build and run container
- `just package` - Build package
- `just document` - Generate package documentation

### Development Workflow

1. **Start New Feature**:
   ```bash
   just version-new-branch  # Create feature branch
   ```

2. **Make Changes**: Develop your feature following the established patterns

3. **Commit Changes**:
   ```bash
   just version  # Use semantic commit messages
   ```

4. **Push and Review**: Create merge/pull request to development branch

## Project Structure

```
your_project/
├── .venv/                          # Virtual environment with Python interpreter
├── automation/                     # Detailed just settings for easier use of terminal commands
├── config/                         # Configuration yaml files that should contain the settings for your package/system
├── data/                           # Data folder to save local data [OPTIONAL - could be removed]
├── docs/                           # Folder to store documentation for package use
├── experiments/                    # Folder to store experiment runs such as mlruns from mlflow [OPTIONAL - could be removed]
├── notebooks/                      # Folder to store .ipynb notebooks [OPTIONAL - could be removed]
├── src/your_project                # Source code
├── tests/                          # Test files
├── .env.example                    # Environment file can be used during development, prefer the use of configs (Remove .example before use)
├── .pre-commit-config.yaml         # Pre commit hook configuration
├── .copier-answers.yaml            # Template update configuration DO NOT EDIT!
├── your_project.code-workspace     # Preconfigured VSCode workspace settings
├── Dockerfile                      # Container image recipe
├── justfile                        # Main terminal command automation file, uses automation/ folder logic
├── pyproject.toml                  # Project configuration
└── README                          # Main README for future package or system
```

## Troubleshooting

### Common Issues

**Python Interpreter Not Found**:
- Ensure `uv sync` completed successfully
- Manually select interpreter: Ctrl+Shift+P → "Python: Select Interpreter"

**Just Commands Not Working**:
- Verify you're in the correct directory
- Ensure Bash terminal is being used
- Check that `just` is installed: `uv tool install just`

**Git Push Fails**:
- Check status and see what git recommends: `git status`
- Verify remote URL is correct: `git remote -v`
- Ensure you have push permissions to the repository

## Support

- 📚 **Documentation**: [Link to detailed docs]
-
---

**Next Steps**: After completing this setup, refer to the detailed documentation for specific deployment and development workflows.
