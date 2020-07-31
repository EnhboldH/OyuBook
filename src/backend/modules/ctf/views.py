from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth import views
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.db.models import Q

from modules.base.models import (
    OyuUser,
    OyuUserProfile,
    CtfChallenge,
    CtfChallengeRequest,
    UserChallenge,
)
from modules.base.forms import (
    CTFChallengeRequestForm,
)
class CTFHomeView(View):
    context = {
        'title': 'Нүүр Хуудас | Capture The Flag',
    }

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.context['profile'] = self.get_profile_data(oyu_user=request.user)
            if request.user.user_type == 'admin':
                self.context['challenge_request_count'] = CtfChallengeRequest.objects.count()

        return render(request, 'ctf/index.html', self.context)

    def post(self, request, *args, **kwargs):
        return render(request, 'ctf/index.html', self.context)

    def get_profile_data(self, oyu_user):

        profile = OyuUserProfile.objects.filter(oyu_user=oyu_user).first()
        if not profile:
            return {}
        return profile

class CTFChallengesView(View):
    context = {
        'title': 'Capture The Flag | Бодлогууд',
    }

    def get(self, request, *args, **kwargs):
        self.context['challenges'] = CtfChallenge.objects.all()
        return render(request, 'ctf/challenges.html', self.context)

    def post(self, request, *args, **kwargs):
        return render(request, 'ctf/challenges.html', self.context)

class CTFChallengeRequestView(SuccessMessageMixin, FormView):
    template_name = 'ctf/challenge-request.html'
    model = CtfChallengeRequest
    form_class = CTFChallengeRequestForm
    success_url = '/ctf/challenge/request'
    success_message = "Бид таны бодлогыг шалгаж үзээд таньд мэдэгдэх болно"

    extra_context = {
        'title': 'Бодлого нэмэх | Capture The Flag',
    }

    def form_valid(self, form):
        challenge_data = form.cleaned_data
        challenge_request = CtfChallengeRequest()
        challenge_request.title = challenge_data.get('title')
        challenge_request.description = challenge_data.get('description')
        challenge_request.category = challenge_data.get('category')
        challenge_request.solution = challenge_data.get('solution')
        challenge_request.flag = challenge_data.get('flag')
        challenge_request.oyu_user = self.request.user
        challenge_request.save()

        return super().form_valid(form)


class CTFScoreboardView(View):
    context = {
        'title': 'Онооны самбар | Capture The Flag',
    }

    def get(self, request, *args, **kwargs):
        return render(request, 'ctf/scoreboard.html', self.context)


class CTFAdminChallengeRequestsView(View):
    context = {
        'title': 'Админ | Capture The Flag',
    }

    def get(self, request, *args, **kwargs):
        self.context['challenges'] = CtfChallengeRequest.objects.all()
        return render(request, 'ctf/admin/admin-challenge-requests.html', self.context)

    def post(self, request, *args, **kwargs):
        challenge_id = request.POST['challenge']
        challenge = CtfChallengeRequest.objects.get(pk=challenge_id)
        req_user = challenge.oyu_user
        CtfChallenge.objects.create(
            title=challenge.title,
            description=challenge.description,
            category=challenge.category,
            flag=challenge.flag
        ).save()
        challenge.delete()
        ctf_chall = CtfChallenge.objects.last()
        UserChallenge.objects.create(
            oyu_user=req_user,
            challenge=ctf_chall,
        ).save()
        self.context['challenges'] = CtfChallengeRequest.objects.all()
        return render(request, 'ctf/admin/admin-challenge-requests.html', self.context)