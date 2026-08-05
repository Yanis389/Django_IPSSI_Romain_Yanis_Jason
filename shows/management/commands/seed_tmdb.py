import os
import requests
from django.core.management.base import BaseCommand
from shows.models import Show

class Command(BaseCommand):
    help = "Scrape TMDB pour peupler la base de données avec des séries réelles."

    def add_arguments(self, parser):
        parser.add_argument('--pages', type=int, default=5, help='Nombre de pages TMDB à récupérer.')

    def handle(self, *args, **options):
        api_key = os.environ.get('TMDB_API_KEY')
        if not api_key:
            self.stderr.write(self.style.ERROR("Erreur: La variable TMDB_API_KEY n'est pas définie dans ton environnement."))
            return

        pages_to_fetch = options['pages']
        base_url = "https://api.themoviedb.org/3"
        
        # 1. Récupération des genres
        genre_res = requests.get(f"{base_url}/genre/tv/list", params={"api_key": api_key, "language": "fr-FR"})
        genre_map = {g['id']: g['name'] for g in genre_res.json().get('genres', [])} if genre_res.status_code == 200 else {}

        self.stdout.write(f"Scraping de {pages_to_fetch} pages depuis TMDB en cours...")
        shows_created = 0

        # 2. Récupération des séries populaires
        for page in range(1, pages_to_fetch + 1):
            pop_res = requests.get(f"{base_url}/tv/popular", params={"api_key": api_key, "language": "fr-FR", "page": page})
            if pop_res.status_code != 200:
                self.stderr.write(self.style.WARNING(f"Échec de la récupération de la page {page}"))
                continue

            for item in pop_res.json().get('results', []):
                tmdb_id = item['id']
                
                # Détails complémentaires pour le statut, les saisons, etc.
                detail_res = requests.get(f"{base_url}/tv/{tmdb_id}", params={"api_key": api_key, "language": "fr-FR"})
                detail_data = detail_res.json() if detail_res.status_code == 200 else {}

                genres_names = [genre_map.get(gid) for gid in item.get('genre_ids', []) if gid in genre_map]
                poster_path = item.get('poster_path') or detail_data.get('poster_path')
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
                run_time_list = detail_data.get('episode_run_time') or [0]

                # 3. Sauvegarde en base de données
                show, created = Show.objects.update_or_create(
                    tmdb_id=tmdb_id,
                    defaults={
                        'title': item.get('name') or detail_data.get('name', 'Titre inconnu'),
                        'original_title': item.get('original_name') or detail_data.get('original_name', ''),
                        'synopsis': item.get('overview') or detail_data.get('overview', ''),
                        'poster_url': poster_url,
                        'genres': genres_names,
                        'first_air_date': item.get('first_air_date') or None,
                        'vote_average': item.get('vote_average', 0.0),
                        'vote_count': item.get('vote_count', 0),
                        'popularity': item.get('popularity', 0.0),
                        'number_of_seasons': detail_data.get('number_of_seasons', 1),
                        'number_of_episodes': detail_data.get('number_of_episodes', 0),
                        'episode_run_time': run_time_list[0] if run_time_list else 0,
                        'status': detail_data.get('status', 'Inconnu'),
                        'original_language': item.get('original_language', 'fr'),
                    }
                )
                
                if created:
                    shows_created += 1

        self.stdout.write(self.style.SUCCESS(f"Seed terminé ! {shows_created} nouvelles séries importées. Total en base : {Show.objects.count()}."))