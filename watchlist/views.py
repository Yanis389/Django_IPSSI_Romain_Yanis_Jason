from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
