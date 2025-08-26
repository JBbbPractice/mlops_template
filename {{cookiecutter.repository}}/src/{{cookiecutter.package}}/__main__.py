# ONLY FOR PACKAGE LOGIC
# Import statements
import typer
from {{cookiecutter.package}} import application

# Entry point of package runs workflow
if __name__ == "__main__":
    typer.run(application.main)
