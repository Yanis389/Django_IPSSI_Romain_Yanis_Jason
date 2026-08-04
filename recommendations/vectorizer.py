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
