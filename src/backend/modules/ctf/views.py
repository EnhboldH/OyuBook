from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth import views
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q

from modules.base.models import (
    OyuUser,
    CtfChallenge,
)
from modules.base.forms import (
    CTFAddChallengeForm,
)
class CTFHomeView(View):
    context = {
        'title': 'Capture The Flag | Нүүр Хуудас',
    }

    def get(self, request, *args, **kwargs):
        return render(request, 'ctf/index.html', self.context)

    def post(self, request, *args, **kwargs):
        return render(request, 'ctf/index.html', self.context)

class CTFChallengesView(View):
    context = {
        'title': 'Capture The Flag | Бодлогууд',
        'challenges': CtfChallenge.objects.all(),
    }

    def get(self, request, *args, **kwargs):
        return render(request, 'ctf/challenges.html', self.context)

    def post(self, request, *args, **kwargs):
        return render(request, 'ctf/challenges.html', self.context)

class CTFChallengeRequestView(View):
    # Change me to FormView

    context = {
        'title': 'test'
    }
    def get(self, request, *args, **kwargs):
        return render(request, 'ctf/challenge-request.html', self.context)
class CTFScoreboardView(View):
    context = {
        'title': 'Capture The Flag | Бодлогууд',
    }

    def get(self, request, *args, **kwargs):
        return render(request, 'ctf/scoreboard.html', self.context)

