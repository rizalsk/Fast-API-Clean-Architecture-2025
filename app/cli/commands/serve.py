# app/cli/commands/serve.py
import typer
import subprocess
from app.cli.app import cli
from app.core.config.app import app_config

@cli.command("serve:dev")
def serve_dev():
    """
    Serve the app in development mode with auto-reload.
    """
    typer.echo(f"Starting development server at http://{app_config.APP_URL}:{app_config.APP_PORT}")
    subprocess.run([
        "uvicorn",
        "app.main:app",
        "--reload",
        "--host", app_config.APP_URL,
        "--port", str(app_config.APP_PORT)
    ])


@cli.command("serve:prod")
def serve_prod(workers: int = 4):
    """
    Serve the app in production mode.
    """
    typer.echo(f"Starting production server at http://{app_config.APP_URL}:{app_config.APP_PORT} with {workers} workers")
    subprocess.run([
        "gunicorn",
        "app.main:app",
        "-k", "uvicorn.workers.UvicornWorker",
        "-w", str(workers),
        "-b", f"{app_config.APP_URL}:{app_config.APP_PORT}"
    ])
