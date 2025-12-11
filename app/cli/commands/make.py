import typer
import os
from app.cli.app import cli
make_app = typer.Typer(help="Generate scaffolding")

@cli.command("make:module")
def make_module(name: str):
    """Generate new module structure like Permission/Article"""
    base = f"app/modules/{name.lower()}"
    folders = ["models", "schemas", "services", "repositories", "routes", "utils"]

    typer.echo(f"📦 Creating module: {name}")

    os.makedirs(base, exist_ok=True)
    for f in folders:
        os.makedirs(f"{base}/{f}", exist_ok=True)
        open(f"{base}/{f}/__init__.py", "w").close()

    typer.echo(f"✅ Module {name} created.")

@cli.command("make:model")
def make_model(name: str):
    """Generate SQLAlchemy model"""
    model_name = name.capitalize()
    file_name = name.lower()
    path = f"app/models/{file_name}.py"

    if os.path.exists(path):
        typer.echo(f"❌ Model {model_name} already exists.")
        raise typer.Exit()

    os.makedirs("app/models", exist_ok=True)
    content = f'''
from sqlalchemy import Column, Integer, String, DateTime
from app.database.base import Base
from datetime import datetime

class {model_name}(Base):
    __tablename__ = "{file_name}"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
'''
    with open(path, "w") as f:
        f.write(content.strip())

    typer.echo(f"✅ Model created: {path}")

@cli.command("make:migration")
def make_migration(name: str):
    """Generate migration via alembic"""
    os.system(f'alembic revision --autogenerate -m "{name}"')
