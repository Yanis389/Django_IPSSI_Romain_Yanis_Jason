import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

FRENCH_STOP_WORDS = [
    "le", "la", "les", "un", "une", "des", "de", "du", "et", "à", "au", "aux",
    "en", "dans", "pour", "avec", "sur", "par", "est", "sont", "qui", "que",
    "ce", "cette", "ces", "son", "sa", "ses", "il", "elle", "ils", "elles",
    "se", "leur", "leurs", "plus", "ne", "pas", "on", "ou", "mais", "d",
    "l", "s", "n", "qu",
]


def fit_vectorizer(synopses):
    vectorizer = TfidfVectorizer(stop_words=FRENCH_STOP_WORDS, max_features=300)
    vectorizer.fit(synopses)
    return vectorizer


def build_show_vectors(vectorizer, synopses):
    return vectorizer.transform(synopses).toarray().tolist()


def cosine_similarity(vector_a, vector_b):
    a = np.array(vector_a, dtype=float)
    b = np.array(vector_b, dtype=float)
    if not a.any() or not b.any():
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def rank_by_similarity(reference_vector, catalog, limit=20):
    scored = [(cosine_similarity(reference_vector, vector), item_id) for item_id, vector in catalog]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [item_id for _, item_id in scored[:limit]]


def update_profile_vector(profile_vector, chosen_vector, rejected_vector, alpha=1.0):
    dim = len(chosen_vector)
    profile = np.array(profile_vector if profile_vector else [0.0] * dim, dtype=float)
    chosen = np.array(chosen_vector, dtype=float)
    rejected = np.array(rejected_vector, dtype=float)
    updated = profile + alpha * (chosen - rejected)
    return updated.tolist()


def recompute_profile_vector(choice_pairs, vector_dim):
    profile = [0.0] * vector_dim
    for chosen_vector, rejected_vector in choice_pairs:
        profile = update_profile_vector(profile, chosen_vector, rejected_vector)
    return profile
