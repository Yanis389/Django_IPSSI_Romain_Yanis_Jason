from django.urls import path

from . import views

urlpatterns = [
    path('duels/', views.onboarding_view, name='duel-onboarding'),
    path('api/duels/pair/', views.DuelPairView.as_view(), name='duel-pair'),
    path('api/duels/choose/', views.DuelChooseView.as_view(), name='duel-choose'),
    path('api/recommendations/', views.RecommendationsView.as_view(), name='recommendations'),
    path('api/profile/genres/', views.GenreBreakdownView.as_view(), name='profile-genres'),
]
