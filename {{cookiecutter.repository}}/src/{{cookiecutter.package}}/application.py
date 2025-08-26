# ACTUAL APPLICATION OR SYSTEM LOGIC
import typer


def main(
    input_path: str = typer.Argument(help="Input"),
    output_dir: str = typer.Argument(help="Output directory"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Verbosity of the output"
    ),
):
    """Workflow documentation"""
    # Start workflow, include output when verbose
    if verbose:
        typer.echo(f"Processing {input_path}")

    # ADD LOGIC

    # End workflow, again include output when verbose
    if verbose:
        typer.echo("Workflow completed.")

    return 0


# For optional cmd execution
if __name__ == "__main__":
    typer.run(main)
