import typer
from app.infrastructure.database.connection import get_database_connection
from app.seeders import users_table_seeder

app = typer.Typer()

@app.command()
def seed():
    """
    Runs the database seeders.
    """
    db_connection = get_database_connection()
    db = db_connection.get_session()
    try:
        users_table_seeder.run(db)
        print("Database seeding completed successfully.")
    except Exception as e:
        db.rollback() # Ensure rollback on error
        print(f"An error occurred during seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    app()