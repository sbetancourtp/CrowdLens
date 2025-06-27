# processing/deck_generator.py

from typing import List
from data.db.main_db import get_all_live_entries
from models.entry_models import EntryRepo
from models.deck_models import DeckRepo
from processing.grouping_engine import group_entries_by_keyword_signature


def generate_decks_from_entries() -> List[DeckRepo]:
    """High-level function to generate DeckRepo objects from unsaved entries."""
    entries: List[EntryRepo] = get_all_live_entries()
    if not entries:
        return []

    decks: List[DeckRepo] = group_entries_by_keyword_signature(entries)
    return decks
