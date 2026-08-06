from rest_framework import serializers

from shows.serializers import ShowListSerializer

from .models import Watchlist, WatchlistEntry


class WatchlistEntrySerializer(serializers.ModelSerializer):
    show = ShowListSerializer(read_only=True)

    class Meta:
        model = WatchlistEntry
        fields = ['id', 'show', 'added_at']


class WatchlistSerializer(serializers.ModelSerializer):
    entries = WatchlistEntrySerializer(many=True, read_only=True)

    class Meta:
        model = Watchlist
        fields = ['id', 'name', 'entries']
