# ACTUAL APPLICATION OR SYSTEM LOGIC
import typer

def main(input: typer.argument(help="Input"), output_dir: typer.argument(help="Output directory"), verbose: bool=typer.Option(False, "--verbose", "-v", help="Verbosity of the output")):
         """Workflow documentation"""
         # Start workflow, include output when verbose
        if verbose:
            typer.echo(f"Processing {input}")

        # ADD LOGIC

        # End workflow, again  include output when verbose
        if verbose:
            typer.echo("Workflow completed.")


# For optional cmd execution
if __name__ == "__main__":
    typer.run(main)
        
