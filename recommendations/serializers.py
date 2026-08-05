from rest_framework import serializers

from .models import UserProfile


class DuelChoiceInputSerializer(serializers.Serializer):
    chosen_id = serializers.IntegerField()
    rejected_id = serializers.IntegerField()

    def validate(self, data):
        if data['chosen_id'] == data['rejected_id']:
            raise serializers.ValidationError("chosen_id et rejected_id doivent être différents.")
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['taste_vector', 'onboarding_completed', 'updated_at']
        read_only_fields = fields
