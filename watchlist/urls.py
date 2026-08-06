from django.urls import path

from . import views

urlpatterns = [
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('watchlists/', views.watchlists, name='watchlists'),
    path('watchlists/<int:pk>/', views.watchlist_detail, name='watchlist-detail'),
    path('watchlists/<int:pk>/entries/', views.watchlist_entries, name='watchlist-entries'),
    path(
        'watchlists/<int:pk>/entries/<int:entry_id>/',
        views.watchlist_entry_detail,
        name='watchlist-entry-detail',
    ),
]
