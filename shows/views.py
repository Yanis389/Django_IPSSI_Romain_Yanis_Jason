import math
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Show
from .serializers import ShowListSerializer, ShowDetailSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class ShowSearchView(APIView):
    """
    GET /api/shows/search/?genre=&year=&min_rating=&status=&language=
    """
    def get(self, request):
        queryset = Show.objects.all().order_by('-popularity')

        genre = request.query_params.get('genre', None)
        if genre:
            queryset = queryset.filter(genres__icontains=genre)

        year = request.query_params.get('year', None)
        if year:
            try:
                year_int = int(year)
                queryset = queryset.filter(first_air_date__year=year_int)
            except ValueError:
                if year.endswith('s') and len(year) == 5:
                    decade_start = int(year[:4])
                    queryset = queryset.filter(
                        first_air_date__year__gte=decade_start,
                        first_air_date__year__lt=decade_start + 10
                    )

        min_rating = request.query_params.get('min_rating', None)
        if min_rating:
            try:
                queryset = queryset.filter(vote_average__gte=float(min_rating))
            except ValueError:
                pass

        status = request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status__iexact=status)

        language = request.query_params.get('language', None)
        if language:
            queryset = queryset.filter(original_language__iexact=language)

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = ShowListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

class ShowDetailView(APIView):
    """
    GET /api/shows/<id>/
    """
    def get(self, request, pk):
        show = get_object_or_404(Show, pk=pk)
        serializer = ShowDetailSerializer(show)
        data = serializer.data

        # Suggestions similaires par cosinus distance sur les feature_vectors
        target_vec = show.feature_vector
        if target_vec and any(target_vec):
            all_shows = Show.objects.exclude(pk=show.pk)
            scored_shows = []
            
            for other in all_shows:
                other_vec = other.feature_vector
                if other_vec and len(other_vec) == len(target_vec):
                    dot = sum(a * b for a, b in zip(target_vec, other_vec))
                    norm_a = math.sqrt(sum(a * a for a in target_vec))
                    norm_b = math.sqrt(sum(b * b for b in other_vec))
                    similarity = dot / (norm_a * norm_b) if norm_a and norm_b else 0.0
                    scored_shows.append((similarity, other))
            
            scored_shows.sort(key=lambda x: x[0], reverse=True)
            top_similar = [item[1] for item in scored_shows[:6]]
            similar_shows = ShowListSerializer(top_similar, many=True).data
        else:
            fallback = Show.objects.exclude(pk=show.pk)
            if show.genres:
                fallback = fallback.filter(genres__icontains=show.genres[0])
            similar_shows = ShowListSerializer(fallback[:6], many=True).data

        data['similar_shows'] = similar_shows
        return Response(data)

def search_page_view(request):
    return render(request, 'shows/search.html')

def detail_page_view(request, pk):
    return render(request, 'shows/detail.html', {'show_id': pk})