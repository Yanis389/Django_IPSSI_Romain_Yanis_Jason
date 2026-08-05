from django.urls import path
from .views import ShowSearchView, ShowDetailView, search_page_view, detail_page_view

urlpatterns = [
    # API
    path('api/shows/search/', ShowSearchView.as_view(), name='api-show-search'),
    path('api/shows/<int:pk>/', ShowDetailView.as_view(), name='api-show-detail'),

    # Front
    path('shows/search/', search_page_view, name='page-show-search'),
    path('shows/<int:pk>/', detail_page_view, name='page-show-detail'),
]