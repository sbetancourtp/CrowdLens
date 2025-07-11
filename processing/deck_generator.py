# processing/deck_generator.py

from typing import List
from data.db.main_db import get_all_live_entries, get_all_live_entries_from_timestamp
from models.entry_models import EntryRepo
from models.deck_models import DeckRepo
from data import shared_state
import time
from processing.grouping_engine import create_decks_by_keyword_signature

CHECK_INTERVAL_SECONDS = 10


def generate_decks_from_entries():
    """High-level function to generate DeckRepo objects from unsaved entries."""

    while True:
        if shared_state.DECKS_UPDATE_TIMESTAMP is None:
            entries: List[EntryRepo] = get_all_live_entries()
            decks: List[DeckRepo] = create_decks_by_keyword_signature(entries)
            with shared_state.decks_lock:
                shared_state.shared_decks.clear()
                shared_state.shared_decks.extend(decks)
        else:
            entries: List[EntryRepo] = get_all_live_entries_from_timestamp()
            decks: List[DeckRepo] = create_decks_by_keyword_signature(entries)
            with shared_state.decks_lock:
                shared_state.shared_decks.extend(decks)

        time.sleep(CHECK_INTERVAL_SECONDS)
        print('Listening Db cycle complete ✅')


def update_decks_from_entries() -> List[DeckRepo]:
    pass
