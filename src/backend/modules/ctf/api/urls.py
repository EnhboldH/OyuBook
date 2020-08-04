from django.urls import path
from .views import ChallengeListView

# For future
urlpatterns = [
    path('challenges/', ChallengeListView.as_view())
]