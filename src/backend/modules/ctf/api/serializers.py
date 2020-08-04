from rest_framework import serializers
from modules.base.models import (
    CtfChallenge,
)

# For future
class CTFChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CtfChallenge
        fields = ('title', 'author', 'category', 'description', 'value', 'state', 'flag', 'solved_users_count')