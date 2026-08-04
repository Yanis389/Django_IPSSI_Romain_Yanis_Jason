from django.test import TestCase

from .vectorizer import build_show_vectors, cosine_similarity, fit_vectorizer, rank_by_similarity


class VectorizerTests(TestCase):
    def setUp(self):
        self.corpus = [
            "Un professeur de chimie malade fabrique de la drogue avec un ancien eleve",
            "Un groupe d'amis se retrouve chaque semaine dans un cafe a New York",
            "Des enfants affrontent des monstres venus d'un monde parallele",
        ]
        self.vectorizer = fit_vectorizer(self.corpus)
        self.vectors = build_show_vectors(self.vectorizer, self.corpus)

    def test_vectors_match_corpus(self):
        self.assertEqual(len(self.vectors), len(self.corpus))

    def test_similarity(self):
        self.assertAlmostEqual(cosine_similarity(self.vectors[0], self.vectors[0]), 1.0)

    def test_ranking(self):
        catalog = list(enumerate(self.vectors))
        self.assertEqual(rank_by_similarity(self.vectors[0], catalog)[0], 0)
