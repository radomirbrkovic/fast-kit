#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os


def run_command(command, cwd=None):
    """Execute shell command with live output."""
    process = subprocess.Popen(command, shell=True, cwd=cwd, executable="/bin/bash")
    process.communicate()
    if process.returncode != 0:
        sys.exit(process.returncode)

def get_paths():
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    venv_python = os.path.join(project_root, "venv", "bin", "python")
    return project_root, venv_python


def install_dependencies():
    print("📦 Installing dependencies...")
    run_command("source venv/bin/activate && pip install -r requirements.txt")


def run_database():
    print("🐳 Starting database via Docker Compose...")
    run_command("docker compose up -d")


def run_server():
    print("🚀 Running FastAPI server...")
    run_command("source venv/bin/activate && uvicorn main:app --reload")


def generate_migrations():
    print("🧩 Generating migrations...")
    run_command("source venv/bin/activate && alembic revision --autogenerate -m 'Auto migration'")


def execute_migrations():
    print("📂 Applying migrations...")
    run_command("source venv/bin/activate && alembic upgrade head")


def rollback_migration():
    print("⏪ Rolling back last migration...")
    run_command("source venv/bin/activate && alembic downgrade -1")


def execute_seeder():
    print("🌱 Running seeders...")
    run_command("source venv/bin/activate && python app/db/seeders/main.py")


def update_project():
    print("⬆️ Checking for updates...")
    run_command("git fetch")
    run_command("git pull")
    print("✅ Project updated to the latest version.")


def main():
    parser = argparse.ArgumentParser(prog="fastkit", description="FastKit CLI utility tool")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("install", help="Install project dependencies")
    subparsers.add_parser("db", help="Run database containers (Docker)")
    subparsers.add_parser("run", help="Run FastAPI development server")
    subparsers.add_parser("makemigrations", help="Generate Alembic migrations")
    subparsers.add_parser("migrate", help="Apply database migrations")
    subparsers.add_parser("rollback", help="Rollback last migration")
    subparsers.add_parser("seed", help="Execute seeders")
    subparsers.add_parser("update", help="Pull latest version from git")

    args = parser.parse_args()

    if args.command == "install":
        install_dependencies()
    elif args.command == "db":
        run_database()
    elif args.command == "run":
        run_server()
    elif args.command == "makemigrations":
        generate_migrations()
    elif args.command == "migrate":
        execute_migrations()
    elif args.command == "rollback":
        rollback_migration()
    elif args.command == "seed":
        execute_seeder()
    elif args.command == "update":
        update_project()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
