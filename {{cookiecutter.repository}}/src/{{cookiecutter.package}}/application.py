"""
Core application logic for the CLI.
"""

import typer

app = typer.Typer()


@app.command()
def main(
    files: list[str] = typer.Argument(
        None, help="Config files for the workflow (local path only)."
    ),
) -> int:
    if len(files) == 0:
        raise RuntimeError("No configs provided.")
    # Add logic
    return 0
