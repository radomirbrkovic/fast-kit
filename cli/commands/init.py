import shutil
import subprocess
from pathlib import Path
import typer

app = typer.Typer(help="Initialize FastKit environment")

@app.command()
def env():
    """
    Initialize the project:
    - Copy .env.example to .env
    - Create virtual environment
    - Install dependencies
    """
    project_root = Path(__file__).resolve().parents[3]
    env_example = project_root / ".env.example"
    env_target = project_root / ".env"
    venv_dir = project_root / "venv"

    if not env_target.exists():
        if env_example.exists():
            shutil.copy(env_example, env_target)
            typer.echo("✅ .env file created from .env.example")
        else:
            typer.echo("⚠️  No .env.example found.")
    else:
        typer.echo("ℹ️  .env file already exists.")

    if not venv_dir.exists():
        typer.echo("🔧 Creating virtual environment...")
        subprocess.run(["python3", "-m", "venv", str(venv_dir)], check=True)
        typer.echo("✅ Virtual environment created.")
    else:
        typer.echo("ℹ️  Virtual environment already exists.")

    typer.echo("📦 Installing dependencies...")
    subprocess.run([str(venv_dir / "bin" / "pip"), "install", "-r", "requirements.txt"], check=True)
    typer.echo("✅ Dependencies installed successfully.")
