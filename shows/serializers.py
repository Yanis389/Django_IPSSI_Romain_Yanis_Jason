from rest_framework import serializers
from .models import Show

class ShowListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = [
            'id', 'tmdb_id', 'title', 'original_title', 'poster_url', 
            'genres', 'first_air_date', 'vote_average', 'vote_count', 
            'popularity', 'original_language'
        ]

class ShowDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = [
            'id', 'tmdb_id', 'title', 'original_title', 'synopsis', 
            'poster_url', 'genres', 'first_air_date', 'vote_average', 
            'vote_count', 'popularity', 'number_of_seasons', 
            'number_of_episodes', 'episode_run_time', 'status', 
            'original_language', 'feature_vector'
        ]