# delete_mock_data_db.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "data/db/crowdlens.db"


def delete_mock_entries():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM entries
            WHERE username = 'mock_user_script_50_entries'
        """)
        deleted = cursor.rowcount
        conn.commit()
    print(f"🗑️ {deleted} mock entries deleted.")


if __name__ == "__main__":
    delete_mock_entries()
