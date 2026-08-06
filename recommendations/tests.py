from django.test import TestCase

from .genre_utils import split_scifi_fantasy
from .vectorizer import (
    build_show_vectors,
    cosine_similarity,
    fit_vectorizer,
    rank_by_similarity,
    recompute_profile_vector,
    update_profile_vector,
)


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

    def test_profile_update(self):
        updated = update_profile_vector(None, self.vectors[0], self.vectors[1])
        self.assertEqual(len(updated), len(self.vectors[0]))

    def test_recompute_matches_replayed_updates(self):
        pairs = [(self.vectors[0], self.vectors[1]), (self.vectors[2], self.vectors[0])]
        dim = len(self.vectors[0])

        replayed = [0.0] * dim
        for chosen, rejected in pairs:
            replayed = update_profile_vector(replayed, chosen, rejected)

        self.assertEqual(recompute_profile_vector(pairs, dim), replayed)


class GenreSplitTests(TestCase):
    def test_fantasy_synopsis(self):
        genres = split_scifi_fantasy(
            ["Science-Fiction & Fantastique"],
            "Un jeune sorcier doit maitriser la magie pour sauver son royaume des dragons.",
        )
        self.assertEqual(genres, ["Fantastique"])

    def test_scifi_synopsis(self):
        genres = split_scifi_fantasy(
            ["Science-Fiction & Fantastique"],
            "Un robot explore une planete lointaine a bord d'un vaisseau spatial.",
        )
        self.assertEqual(genres, ["Science-Fiction"])

    def test_unclear_synopsis_keeps_combined_tag(self):
        genres = split_scifi_fantasy(["Science-Fiction & Fantastique"], "Une histoire sans indice particulier.")
        self.assertEqual(genres, ["Science-Fiction & Fantastique"])

    def test_untouched_when_tag_absent(self):
        self.assertEqual(split_scifi_fantasy(["Drame"], "peu importe"), ["Drame"])
