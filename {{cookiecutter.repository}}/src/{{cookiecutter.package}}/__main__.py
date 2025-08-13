# ONLY FOR PACKAGE LOGIC
# Import statements
import typer
from {{cookiecutter.package}} import workflow

# Entry point of package runs workflow
if __name__ == "__main__":
    typer.run(worklfow.main)
