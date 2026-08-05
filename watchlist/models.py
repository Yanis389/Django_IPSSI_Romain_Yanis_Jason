from django.contrib.auth.models import User
from django.db import models

from shows.models import Show


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlists')
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.name} ({self.user.username})'


class WatchlistEntry(models.Model):
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name='entries')
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        unique_together = ['watchlist', 'show']

    def __str__(self):
        return f'{self.show.title} dans {self.watchlist.name}'
