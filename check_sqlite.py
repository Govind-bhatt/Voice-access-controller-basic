import sqlite3
from pathlib import Path


def main():
    data_folder = Path("data")
    data_folder.mkdir(exist_ok=True)

    database_path = data_folder / "test.sqlite3"

    connection = sqlite3.connect(database_path)

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS installation_test (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL
        )
        """
    )

    connection.execute(
        "INSERT INTO installation_test (message) VALUES (?)",
        ("SQLite is working",),
    )

    connection.commit()

    row = connection.execute(
        "SELECT id, message FROM installation_test ORDER BY id DESC LIMIT 1"
    ).fetchone()

    connection.close()

    print(f"Database created: {database_path}")
    print(f"Test record: {row}")


if __name__ == "__main__":
    main()
