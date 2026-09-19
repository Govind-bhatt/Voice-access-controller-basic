import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from config import DATABASE_PATH, ensure_project_folders


def get_connection():
    """Open a connection to the local assistant database."""
    ensure_project_folders()
    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    """Create the database tables if they do not already exist."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS command_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                activation_method TEXT NOT NULL,
                command_text TEXT NOT NULL,
                access_granted INTEGER NOT NULL,
                action_result TEXT NOT NULL,
                security_event TEXT
            )
            """
        )
        connection.commit()


def log_command(
    activation_method,
    command_text,
    access_granted,
    action_result,
    security_event=None,
):
    """Save a command result without saving audio or the access code."""
    initialize_database()

    timestamp = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO command_log (
                timestamp,
                activation_method,
                command_text,
                access_granted,
                action_result,
                security_event
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                activation_method,
                command_text,
                int(access_granted),
                action_result,
                security_event,
            ),
        )
        connection.commit()


def get_recent_logs(limit=10):
    """Return recent command and security-event records."""
    initialize_database()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT
                id,
                timestamp,
                activation_method,
                command_text,
                access_granted,
                action_result,
                security_event
            FROM command_log
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )
        return cursor.fetchall()


if __name__ == "__main__":
    initialize_database()

    log_command(
        activation_method="installation-test",
        command_text="database test",
        access_granted=True,
        action_result="SQLite logging is working",
    )

    print(f"Database created: {Path(DATABASE_PATH).resolve()}")
    print("Recent records:")

    for record in get_recent_logs():
        print(record)
