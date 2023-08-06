"""Main Module for Command Line App"""

from typing import Optional

import typer
from typer.main import Typer

from nautilus_namecodes._version import __version__
from nautilus_namecodes.format.generate_console import ConsoleOutput

app: Typer = typer.Typer()


def mutually_exclusive_group(size=2):
    """Helper Function to assure Mutually Exclusive Options are not used."""

    group = set()

    def callback(
        ctx: typer.Context, param: typer.CallbackParam, value: bool
    ):  # pylint: disable=unused-argument
        # Add cli option to group if it was called with a value
        if value is not None and param.name not in group:
            group.add(param.name)
        if len(group) > size - 1:
            raise typer.BadParameter(f"{group} are mutually exclusive")
        return value

    return callback


def version_callback(value: bool) -> None:
    """Simple Callback Function to return the Version Number of the Program"""

    if value:
        typer.echo(f"Namecodes Version: {__version__}")
        raise typer.Exit()


exclusivity_callback = mutually_exclusive_group()


@app.command()
def codes(
    show_tree: bool = typer.Option(
        None,
        "--show-tree",
        help="Print Summary Tree to Console.",
        callback=exclusivity_callback,
    ),
    show_blocks: bool = typer.Option(
        None,
        "--show-blocks",
        help="Print Blocks with Codes to Console.",
        callback=exclusivity_callback,
    ),
    show_codes: bool = typer.Option(
        None,
        "--show-codes",
        help="Print Codes to Console.",
        callback=exclusivity_callback,
    ),
) -> None:
    """Command for the Management of Name Codes"""

    if not any([show_tree, show_blocks, show_codes]):
        raise typer.BadParameter(
            "Required to specify either: --show-tree, --show-blocks, --show-codes, ."
        )

    if show_tree:
        typer.echo(ConsoleOutput.generate_tree_output())

    if show_blocks:
        typer.echo(ConsoleOutput.generate_blocks_output())

    if show_codes:
        typer.echo(ConsoleOutput.generate_codes_output())


@app.callback()
def main(
    version: Optional[bool] = typer.Option(  # pylint: disable=unused-argument
        None, "--version", callback=version_callback
    ),
):
    """Main Function of CLI application, defining main options."""
    return


if __name__ == "__main__":
    app()
