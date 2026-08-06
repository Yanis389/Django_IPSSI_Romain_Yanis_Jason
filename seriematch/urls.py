from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/shows/search/', permanent=False)),
    path('admin/', admin.site.urls),
    path('', include('recommendations.urls')),
    path('', include('shows.urls')),
    path('', include('watchlist.urls')),
]