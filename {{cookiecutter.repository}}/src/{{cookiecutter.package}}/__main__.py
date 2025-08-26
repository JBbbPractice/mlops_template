"""
Entry point for the CLI application.
"""
import sys
from {{cookiecutter.package}}.application import app

if __name__ == "__main__":
    sys.exit(app())