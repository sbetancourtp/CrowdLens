import sqlite3
from pathlib import Path
from models.entry_models import EntryRepo

# Use the current directory (same where this file is located)
DB_PATH = Path(__file__).parent / "crowdlens.db"


def initialize_db():
    """Initialize the SQLite database and create tables if they do not exist."""
    should_create = not DB_PATH.exists()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS decks (
            deck_id TEXT PRIMARY KEY,
            first_entry_date TEXT NOT NULL,
            last_entry_date TEXT NOT NULL,
            provided_keywords TEXT,
            generated_keywords TEXT,
            all_entries_summary_sentence TEXT,
            save_flag INTEGER NOT NULL,
            priority INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            entry_id TEXT PRIMARY KEY,
            user_id TEXT,
            username TEXT,
            message_id INTEGER,
            text TEXT,
            timestamp TEXT,
            deck_id TEXT,
            save_flag INTEGER NOT NULL,
            FOREIGN KEY(deck_id) REFERENCES decks(deck_id)
        )
    """)

    conn.commit()
    conn.close()

    if should_create:
        print("✔️ Database created and initialized.")
    else:
        print("ℹ️ Database already exists. Tables ensured.")


def write_entry_to_db(entry: EntryRepo) -> None:
    """Insert an Entry object into the entries table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO entries (
            entry_id, user_id, username,
            message_id, text, timestamp, deck_id, save_flag
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        entry.entry_id,
        str(entry.user_id),
        entry.username,
        entry.message_id,
        entry.text,
        entry.timestamp.isoformat(),
        entry.deck_id,
        int(entry.save_flag)  # SQLite doesn't have boolean: use 0 or 1
    ))

    conn.commit()
    conn.close()
