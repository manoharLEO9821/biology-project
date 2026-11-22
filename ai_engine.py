import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from biomimicry_data import BIOMIMICRY_DATA


def _build_corpus(data):
    return [
        f"{item.get('name', '')} {item.get('category', '')} "
        f"{item.get('mechanism', '')} {item.get('engineering', '')} "
        f"{item.get('problem', '')}"
        for item in data
    ]


_CORPUS = _build_corpus(BIOMIMICRY_DATA)
_VECTORIZER = TfidfVectorizer(stop_words="english")
_TFIDF_MATRIX = _VECTORIZER.fit_transform(_CORPUS) if _CORPUS else None


def recommend_solutions(query: str, top_k: int = 5):
    if not query or not query.strip() or not BIOMIMICRY_DATA or _TFIDF_MATRIX is None:
        return []

    query_vec = _VECTORIZER.transform([query.strip()])
    scores = cosine_similarity(query_vec, _TFIDF_MATRIX).flatten()
    ranked_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for idx in ranked_indices:
        item = dict(BIOMIMICRY_DATA[int(idx)])
        item["similarity"] = float(max(0.0, min(1.0, scores[int(idx)])))
        results.append(item)
    return results