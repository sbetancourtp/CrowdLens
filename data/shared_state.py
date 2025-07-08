# data/shared_state.py

from threading import Lock
from typing import List, Optional
from datetime import datetime
from models.deck_models import DeckRepo

shared_decks: List[DeckRepo] = []
decks_lock = Lock()
unused_signature_to_entries: list[tuple] = list()

DECKS_UPDATE_TIMESTAMP: Optional[datetime] = None
