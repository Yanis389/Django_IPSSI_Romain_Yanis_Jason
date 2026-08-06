from django.urls import path

from . import views

urlpatterns = [
    path('api/auth/register/', views.register, name='register'),
    path('api/auth/login/', views.login_view, name='login'),
    path('api/auth/logout/', views.logout_view, name='logout'),
    path('api/watchlists/', views.watchlists, name='watchlists'),
    path('api/watchlists/<int:pk>/', views.watchlist_detail, name='watchlist-detail'),
    path('api/watchlists/<int:pk>/entries/', views.watchlist_entries, name='watchlist-entries'),
    path(
        'api/watchlists/<int:pk>/entries/<int:entry_id>/',
        views.watchlist_entry_detail,
        name='watchlist-entry-detail',
    ),

    path('accueil/', views.home_page, name='page-home'),
    path('connexion/', views.login_page, name='page-login'),
    path('watchlists/', views.watchlists_page, name='page-watchlists'),
]
