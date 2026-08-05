from sklearn.feature_extraction.text import TfidfVectorizer

def fit_vectorizer(synopses, max_features=50):
    """Ajuste le modèle TF-IDF sur la liste des synopsis."""
    vectorizer = TfidfVectorizer(max_features=max_features, stop_words='french')
    if synopses and any(s.strip() for s in synopses):
        vectorizer.fit(synopses)
    return vectorizer

def build_show_vectors(vectorizer, synopses):
    """Transforme les synopsis en listes de floats (vecteurs)."""
    if not synopses or not hasattr(vectorizer, 'vocabulary_'):
        return [[0.0] * 50 for _ in synopses]
    matrix = vectorizer.transform(synopses)
    return matrix.toarray().tolist()