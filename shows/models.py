from django.db import models

class Show(models.Model):
    tmdb_id = models.IntegerField(unique=True, db_index=True)
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)
    poster_url = models.URLField(max_length=500, blank=True, null=True)
    genres = models.JSONField(default=list, help_text="Liste des noms de genres")
    first_air_date = models.DateField(blank=True, null=True)
    vote_average = models.FloatField(default=0.0)
    vote_count = models.IntegerField(default=0)
    popularity = models.FloatField(default=0.0)
    number_of_seasons = models.IntegerField(default=1)
    number_of_episodes = models.IntegerField(default=0)
    episode_run_time = models.IntegerField(default=0, help_text="Durée moyenne d'un épisode en minutes")
    status = models.CharField(max_length=50, blank=True, null=True)
    original_language = models.CharField(max_length=10, default="fr")
    feature_vector = models.JSONField(default=list, help_text="Vecteur TF-IDF des synopsis")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-popularity']

    def __str__(self):
        return self.title