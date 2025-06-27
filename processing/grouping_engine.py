from collections import defaultdict, Counter
from typing import List
from uuid import uuid4
from models.entry_models import EntryRepo
from models.deck_models import DeckRepo
from processing.keyword_extraction import extract_keywords

MIN_KEYWORDS_PER_SIGNATURE = 2  # Minimum number of keywords to form a deck signature
MAX_KEYWORDS_PER_SIGNATURE = 5  # Maximum number of keywords to form a deck signature
MIN_ENTRIES_PER_DECK = 5        # Minimum number of entries to form a deck


def group_entries_by_keyword_signature(entries: List[EntryRepo]) -> List[DeckRepo]:
    """
    Group entries into decks based on shared keyword signatures (2 to 5 keywords).
    Returns a list of DeckRepo objects.
    """
    if not entries:
        return []

    # Use extract_keywords to get top keywords per entry
    keywords_per_entry = extract_keywords(entries, top_k=MAX_KEYWORDS_PER_SIGNATURE)

    # Count keyword frequencies across all entries
    keyword_counter = Counter()
    for kws in keywords_per_entry.values():
        keyword_counter.update(kws)

    # Group entries by keyword signature
    signature_to_entries = defaultdict(list)

    for entry in entries:
        keywords = keywords_per_entry.get(entry.entry_id, [])
        if len(keywords) < MIN_KEYWORDS_PER_SIGNATURE:
            continue
        keywords = sorted(set(keywords), key=lambda k: -keyword_counter[k])
        for size in range(MAX_KEYWORDS_PER_SIGNATURE, MIN_KEYWORDS_PER_SIGNATURE - 1, -1):
            if len(keywords) >= size:
                signature = tuple(sorted(keywords[:size]))
                signature_to_entries[signature].append(entry)
                break  # Assign to the most specific signature

    # Build DeckRepo objects
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

    return decks
