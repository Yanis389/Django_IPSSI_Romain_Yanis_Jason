# Contrat API — SérieMatch

Ce fichier fixe les endpoints et formats attendus AVANT que chacun code sa
partie, pour que le frontend et les autres apps puissent avancer sans
s'attendre. Si un format doit changer en cours de route, on le modifie ici
d'abord et on prévient les autres.

## Personne 1 — Données & Recherche (app `shows`)

- `GET /api/shows/search/?genre=&year=&min_rating=&status=&language=`
  → liste paginée de séries
- `GET /api/shows/<id>/`
  → détail d'une série

Format d'une série (`Show`) :
```json
{
  "id": 1,
  "tmdb_id": 1399,
  "title": "...",
  "synopsis": "...",
  "poster_url": "...",
  "genres": ["Drame", "Science-Fiction"],
  "first_air_date": "2011-04-17",
  "vote_average": 8.4,
  "vote_count": 21000,
  "popularity": 512.3,
  "number_of_seasons": 8,
  "number_of_episodes": 73,
  "episode_run_time": 55,
  "status": "Ended",
  "original_language": "en"
}
```

## Personne 2 — Moteur IA (app `recommendations`)

- `GET /api/duels/pair/` → `{ "show_a": Show, "show_b": Show }`
- `POST /api/duels/choose/` body `{ "chosen_id": int, "rejected_id": int }`
  → `{ "taste_vector": [...] }`
- `GET /api/recommendations/` → liste de `Show` (top N pour l'utilisateur connecté)
- `GET /api/recommendations/similar/<show_id>/` → liste de `Show` similaires

## Personne 3 — Compte & Compilation (app `watchlist`)

- `POST /api/auth/register/` body `{ "username": str, "password": str }`
- `POST /api/auth/login/` body `{ "username": str, "password": str }`
- `POST /api/auth/logout/` → vide aussi la watchlist + le profil de goût
- `GET /api/watchlist/` → liste de `{ "id": int, "show": Show, "added_at": str }`
- `POST /api/watchlist/` body `{ "show_id": int }`
- `DELETE /api/watchlist/<id>/`

## Règles communes

- Toutes les routes API sont préfixées par `/api/` (voir `seriematch/urls.py`)
- Auth par session Django (cookie), pas de JWT pour l'instant — plus simple à 3
- Chaque app expose son propre `urls.py`, inclus dans `seriematch/urls.py`
- Si vous changez un format de réponse, mettez à jour ce fichier dans le même commit
