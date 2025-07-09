from collections import defaultdict, Counter
from typing import List, Dict
from uuid import uuid4

from data import shared_state
from models.entry_models import EntryRepo
from models.deck_models import DeckRepo
from processing.keyword_extraction import extract_keywords

MIN_KEYWORDS_PER_SIGNATURE = 2  # Minimum number of keywords to form a deck signature
MAX_KEYWORDS_PER_SIGNATURE = 5  # Maximum number of keywords to form a deck signature
MIN_ENTRIES_PER_DECK = 5        # Minimum number of entries to form a deck


def create_decks_by_keyword_signature(entries: List[EntryRepo]) -> List[DeckRepo]:
    if not entries:
        return []

    keywords_per_entry: Dict[str, List[str]] = extract_keywords(entries, top_k=MAX_KEYWORDS_PER_SIGNATURE)

    keyword_frequency_counter = Counter()
    for kws in keywords_per_entry.values():
        keyword_frequency_counter.update(kws)

    # Initialize dict with all signature->entries already known
    signature_to_entries = defaultdict(list)

    for old_signature, old_entries in shared_state.unused_signature_to_entries:
        signature_to_entries[old_signature].extend(old_entries)

    # Clear unused_signature_to_entries to start from zero
    shared_state.unused_signature_to_entries.clear()

    # Group new entries
    for entry in entries:
        keywords = keywords_per_entry.get(entry.entry_id, [])
        if len(keywords) < MIN_KEYWORDS_PER_SIGNATURE:
            continue
        freq_sorted_kwds = sorted(set(keywords), key=lambda k: -keyword_frequency_counter[k])
        for size in range(MAX_KEYWORDS_PER_SIGNATURE, MIN_KEYWORDS_PER_SIGNATURE - 1, -1):
            if len(freq_sorted_kwds) >= size:
                signature = tuple(sorted(freq_sorted_kwds[:size]))
                signature_to_entries[signature].append(entry)
                break

    # Build decks or save incomplete entry groups
    decks = []
    for signature, grouped_entries in signature_to_entries.items():
        if len(grouped_entries) >= MIN_ENTRIES_PER_DECK:
            sorted_entries = sorted(grouped_entries, key=lambda e: e.timestamp)
            deck = DeckRepo(
                deck_id=uuid4(),
                deck_title=" / ".join(signature),
                first_entry_date=sorted_entries[0].timestamp,
                last_entry_date=sorted_entries[-1].timestamp,
                provided_keywords=[],
                generated_keywords=list(signature),
                entries_list=sorted_entries,
                amount=len(sorted_entries),
                save_flag=False,
                priority=50,
            )
            decks.append(deck)
        else:
            shared_state.unused_signature_to_entries.append((signature, grouped_entries))

    return decks
