import typer
from cli.commands import init

app = typer.Typer(help="⚡ FastKit CLI — Manage your FastKit app easily.")

app.add_typer(init.app, name="init")

if __name__ == "__main__":
    app()
