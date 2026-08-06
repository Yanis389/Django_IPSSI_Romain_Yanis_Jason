from django.core.management.base import BaseCommand

from shows.models import Show

from recommendations.models import DuelChoice, UserProfile
from recommendations.vectorizer import recompute_profile_vector


class Command(BaseCommand):
    help = "Recalcule le taste_vector de chaque profil a partir de l'historique des duels."

    def handle(self, *args, **options):
        sample = Show.objects.exclude(feature_vector=[]).first()
        if not sample:
            self.stderr.write(self.style.ERROR("Aucune serie avec feature_vector en base."))
            return
        vector_dim = len(sample.feature_vector)

        updated = 0
        for profile in UserProfile.objects.all():
            choices = DuelChoice.objects.filter(user=profile.user).order_by('created_at')
            pairs = []
            for choice in choices:
                chosen_vec = choice.show_chosen.feature_vector
                rejected_vec = choice.show_rejected.feature_vector
                if len(chosen_vec) == vector_dim and len(rejected_vec) == vector_dim:
                    pairs.append((chosen_vec, rejected_vec))

            profile.taste_vector = recompute_profile_vector(pairs, vector_dim)
            profile.save(update_fields=['taste_vector'])
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"{updated} profils recalcules."))
