# data/shared_state.py

from threading import Lock
from typing import List, Optional
from datetime import datetime
from models.deck_models import DeckRepo
from models.entry_models import EntryRepo

shared_decks: List[DeckRepo] = []
clustered_entries: List[EntryRepo] = []
decks_lock = Lock()
unused_signature_to_entries: list[tuple] = list()

DECKS_UPDATE_TIMESTAMP: Optional[datetime] = None
