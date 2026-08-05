from django.urls import path

from . import views

urlpatterns = [
    path('duels/', views.onboarding_view, name='duel-onboarding'),
]
