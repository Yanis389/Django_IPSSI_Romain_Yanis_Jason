from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shows.models import Show

from .models import Watchlist, WatchlistEntry
from .serializers import WatchlistSerializer


@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'username et password sont obligatoires'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': "ce nom d'utilisateur est deja pris"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.create_user(username=username, password=password)
    login(request, user)
    return Response(
        {'id': user.id, 'username': user.username},
        status=status.HTTP_201_CREATED,
    )


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is None:
        return Response(
            {'error': 'identifiants invalides'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    login(request, user)
    return Response({'id': user.id, 'username': user.username})


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'detail': 'deconnecte'})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def watchlists(request):
    if request.method == 'GET':
        listes = Watchlist.objects.filter(user=request.user)
        return Response(WatchlistSerializer(listes, many=True).data)

    name = request.data.get('name')
    if not name:
        return Response(
            {'error': 'name est obligatoire'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    liste = Watchlist.objects.create(user=request.user, name=name)
    return Response(
        WatchlistSerializer(liste).data,
        status=status.HTTP_201_CREATED,
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def watchlist_detail(request, pk):
    liste = get_object_or_404(Watchlist, pk=pk, user=request.user)
    return Response(WatchlistSerializer(liste).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def watchlist_entries(request, pk):
    liste = get_object_or_404(Watchlist, pk=pk, user=request.user)
    show_id = request.data.get('show_id')

    if not show_id:
        return Response(
            {'error': 'show_id est obligatoire'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    show = get_object_or_404(Show, pk=show_id)

    if WatchlistEntry.objects.filter(watchlist=liste, show=show).exists():
        return Response(
            {'error': 'cette serie est deja dans la liste'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    WatchlistEntry.objects.create(watchlist=liste, show=show)
    return Response(
        WatchlistSerializer(liste).data,
        status=status.HTTP_201_CREATED,
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def watchlist_entry_detail(request, pk, entry_id):
    liste = get_object_or_404(Watchlist, pk=pk, user=request.user)
    entree = get_object_or_404(WatchlistEntry, pk=entry_id, watchlist=liste)
    entree.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def home_page(request):
    return render(request, 'watchlist/home.html')


def login_page(request):
    return render(request, 'watchlist/login.html')


def watchlists_page(request):
    return render(request, 'watchlist/watchlists.html')
