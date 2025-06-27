from datetime import datetime
from models.entry_models import EntryRepo


def map_db_to_entryrepo(row: tuple) -> EntryRepo:
    """Map a database row to an EntryRepo object."""
    return EntryRepo(
        entry_id=row[0],
        user_id=int(row[1]),
        username=row[2],
        message_id=int(row[3]),
        text=row[4],
        timestamp=datetime.fromisoformat(row[5]),
        deck_id=row[6],
        save_flag=bool(row[7]),
        media_type='text'
    )
