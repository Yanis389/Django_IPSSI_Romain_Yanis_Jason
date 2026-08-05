from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shows.models import Show
from shows.serializers import ShowListSerializer

from .models import DuelChoice, UserProfile
from .serializers import DuelChoiceInputSerializer
from .vectorizer import update_profile_vector


@ensure_csrf_cookie
def onboarding_view(request):
    return render(request, 'recommendations/onboarding.html')


def genre_overlap(a, b):
    return len(set(a.get('genres') or []) & set(b.get('genres') or []))


def pick_diverse_pair(shows, used_pairs, used_show_ids):
    candidates = []
    for i in range(len(shows)):
        for j in range(i + 1, len(shows)):
            a, b = shows[i], shows[j]
            key = f"{a['id']}-{b['id']}"
            if key in used_pairs:
                continue
            fresh_count = (a['id'] not in used_show_ids) + (b['id'] not in used_show_ids)
            candidates.append((fresh_count, -genre_overlap(a, b), key, a, b))

    if not candidates:
        return None

    candidates.sort(key=lambda c: (c[0], c[1]), reverse=True)
    _, _, key, a, b = candidates[0]
    return key, a, b


class DuelPairView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shows = list(Show.objects.values('id', 'genres'))
        if len(shows) < 2:
            return Response(
                {'detail': "Pas assez de series en base."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        used_pairs = request.session.get('duel_used_pairs', [])
        used_show_ids = set(request.session.get('duel_used_show_ids', []))

        pick = pick_diverse_pair(shows, used_pairs, used_show_ids)
        if pick is None:
            used_pairs = []
            used_show_ids = set()
            pick = pick_diverse_pair(shows, used_pairs, used_show_ids)

        key, a, b = pick
        used_pairs = used_pairs + [key]
        used_show_ids = used_show_ids | {a['id'], b['id']}
        request.session['duel_used_pairs'] = used_pairs
        request.session['duel_used_show_ids'] = list(used_show_ids)

        show_a = Show.objects.get(pk=a['id'])
        show_b = Show.objects.get(pk=b['id'])
        return Response({
            'show_a': ShowListSerializer(show_a).data,
            'show_b': ShowListSerializer(show_b).data,
        })


class DuelChooseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        input_serializer = DuelChoiceInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        chosen = Show.objects.get(pk=input_serializer.validated_data['chosen_id'])
        rejected = Show.objects.get(pk=input_serializer.validated_data['rejected_id'])

        DuelChoice.objects.create(user=request.user, show_chosen=chosen, show_rejected=rejected)

        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.taste_vector = update_profile_vector(
            profile.taste_vector, chosen.feature_vector, rejected.feature_vector,
        )
        profile.save(update_fields=['taste_vector'])

        return Response({'taste_vector': profile.taste_vector})
