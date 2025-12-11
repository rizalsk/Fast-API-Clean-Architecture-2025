import typer
import subprocess
from app.cli.app import cli
from app.database.seeders.db_seeder import run_seeder

@cli.command("db:seed")
def seed_all():
    """Run all seeders"""
    typer.echo("🌱 Running all DB seeders...")
    # subprocess.run(["python", "-m", "app.database.seeders.db_seeder"])
    run_seeder()
    typer.echo("✅ All seeders completed.")

@cli.command("db:migrate")
def migrate():
    """Run alembic migration"""
    typer.echo("🔄 Running migrations...")
    subprocess.run(["alembic", "upgrade", "head"])
    typer.echo("✅ Migration completed.")

@cli.command("db:migrate --revision")
def revision(message: str):
    """Create migration file"""
    typer.echo("📄 Creating migration...")
    subprocess.run(["alembic", "revision", "--autogenerate", "-m", message])
    typer.echo("✅ Migration file created.")
