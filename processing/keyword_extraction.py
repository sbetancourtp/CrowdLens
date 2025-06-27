from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict
from models.entry_models import EntryRepo
import numpy as np
import string
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('english') + stopwords.words('spanish') + stopwords.words('portuguese'))


def clean_text(text: str) -> str:
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text


def is_valid_keyword(word: str) -> bool:
    if not word:
        return False
    if word in STOPWORDS:
        return False
    if len(word) < 3:
        return False
    return True


def extract_keywords(entries: List[EntryRepo], top_k: int = 5) -> Dict[str, List[str]]:
    """
    Given a list of entries, return a dict mapping entry_id to its top TF-IDF keywords.
    """
    docs = [clean_text(e.text or '') for e in entries]
    entry_ids = [e.entry_id for e in entries]

    vectorizer = TfidfVectorizer(stop_words=list(STOPWORDS))
    tfidf_matrix = vectorizer.fit_transform(docs)
    feature_names = vectorizer.get_feature_names_out()

    keywords_per_entry = {}

    for i, entry_id in enumerate(entry_ids):
        # TODO This process should be a function, will need to be used more
        row = tfidf_matrix[i].toarray().flatten()
        top_indices = row.argsort()[-top_k:][::-1]
        keywords = [feature_names[idx] for idx in top_indices if is_valid_keyword(feature_names[idx])]
        keywords_per_entry[entry_id] = keywords

    return keywords_per_entry


def calculate_similarity_matrix(tfidf_matrix) -> np.ndarray:
    return cosine_similarity(tfidf_matrix)


def get_tfidf_matrix(entries: List[EntryRepo]):
    docs = [clean_text(e.text or '') for e in entries]
    vectorizer = TfidfVectorizer(stop_words=list(STOPWORDS))
    tfidf_matrix = vectorizer.fit_transform(docs)
    return tfidf_matrix, vectorizer.get_feature_names_out()
