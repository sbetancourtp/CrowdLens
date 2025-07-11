# crowdlens/semantic_processing/semantic_deck_generator.py
import re
import time
from typing import List, Dict
from uuid import uuid4
from collections import defaultdict, Counter

from models.entry_models import EntryRepo
from models.deck_models import DeckRepo
from data import shared_state
from data.db.main_db import get_all_live_entries_from_timestamp, get_all_live_entries

from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
import nltk
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

model = SentenceTransformer('all-MiniLM-L6-v2')

STOPWORDS = set(stopwords.words('english') + stopwords.words('spanish') + stopwords.words('portuguese'))
CHECK_INTERVAL_SECONDS = 10


def extract_top_keywords(texts: List[str], top_k: int = 5) -> List[str]:
    counter = Counter()
    for text in texts:
        tokens = re.findall(r'\b\w\w+\b', text.lower())
        filtered = [t for t in tokens if t.isalpha() and t not in STOPWORDS and len(t) > 2]
        counter.update(filtered)
    return [kw for kw, _ in counter.most_common(top_k)]


def cluster_entries(entries: List[EntryRepo], eps=0.4, min_samples=2) -> List[DeckRepo]:
    if not entries:
        return []

    texts = [e.text or '' for e in entries]
    entry_ids = [e.entry_id for e in entries]
    embeddings = model.encode(texts, convert_to_tensor=True)

    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine')
    labels = clustering.fit_predict(embeddings.cpu())

    clusters: Dict[int, List[EntryRepo]] = defaultdict(list)
    for entry, label in zip(entries, labels):
        if label != -1:
            clusters[label].append(entry)

    decks = []
    for group_entries in clusters.values():
        sorted_entries = sorted(group_entries, key=lambda e: e.timestamp)
        texts = [e.text or '' for e in group_entries]
        keywords = extract_top_keywords(texts)

        deck = DeckRepo(
            deck_id=uuid4(),
            deck_title=" / ".join(keywords),
            first_entry_date=sorted_entries[0].timestamp,
            last_entry_date=sorted_entries[-1].timestamp,
            provided_keywords=[],
            generated_keywords=keywords,
            entries_list=group_entries,
            amount=len(group_entries),
            save_flag=False,
            priority=50,
        )
        decks.append(deck)

    return decks


def generate_semantic_decks():
    while True:
        if shared_state.DECKS_UPDATE_TIMESTAMP is None:
            new_entries = get_all_live_entries()
        else:
            new_entries = get_all_live_entries_from_timestamp()

        if new_entries:
            # Combine old + new entries
            all_entries = shared_state.clustered_entries + new_entries

            # Run clustering
            new_decks = cluster_entries(all_entries)

            with shared_state.decks_lock:
                shared_state.shared_decks = new_decks  # Replace all decks
                shared_state.clustered_entries = all_entries  # Keep memory of all

        time.sleep(CHECK_INTERVAL_SECONDS)
        print('Semantic deck generator listening Db cycle complete ✅')
