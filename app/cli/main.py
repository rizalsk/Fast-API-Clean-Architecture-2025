import typer
import subprocess
from app.core.config.app import app_config

from app.cli.app import cli

# Import ALL commands so they register themselves
import app.cli.commands.serve
import app.cli.commands.db
import app.cli.commands.make

app = typer.Typer(help=app_config.APP_NAME + " CLI")

def run():
    cli()

if __name__ == "__main__":
    run()
