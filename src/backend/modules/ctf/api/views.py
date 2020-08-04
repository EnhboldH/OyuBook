from modules.base.models import (
    CtfChallenge,
)

from rest_framework.generics import ListAPIView
from .serializers import CTFChallengeSerializer

class ChallengeListView(ListAPIView):
    queryset = CtfChallenge.objects.all()
    serializer_class = CTFChallengeSerializer
