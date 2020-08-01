from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
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
    CTFChallengeSubmitForm,
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
        'title': 'Бодлогууд | Capture The Flag',
        'form': CTFChallengeSubmitForm,
    }

    def get(self, request, *args, **kwargs):
        self.context['challenges'] = CtfChallenge.objects.all()
        self.context['tops'] = OyuUserProfile.objects.order_by('-score')[:5]
        return render(request, 'ctf/challenges.html', self.context)

    def post(self, request, *args, **kwargs):
        self.context['challenges'] = CtfChallenge.objects.all()
        self.context['tops'] = OyuUserProfile.objects.order_by('-score')[:5]
        value = request.POST[list(request.POST)[1]]
        chall_id = list(request.POST)[1].split('-')[1]
        challenge = CtfChallenge.objects.get(pk=chall_id)
        if challenge.flag == value:
            messages.success(request, 'Хариулт зөв байна')
            challenge.solved_users_count += 1
            if request.user.is_authenticated:
                user = OyuUserProfile.objects.filter(oyu_user=request.user).first()
                user.solved_problem += 1
                user.score += challenge.value
                user.save()
            challenge.save()
            return render(request, 'ctf/challenges.html', self.context)
        else:
            messages.error(request, 'Хариулт буруу байна')
            return render(request, 'ctf/challenges.html', self.context)

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

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.INFO, 'Бодлого нэмэхийн тулд та нэвтэрнэ үү',fail_silently=True)
            return redirect('user_login')
        return self.render_to_response(self.get_context_data())

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
        self.context['users'] = OyuUserProfile.objects.order_by('-score')
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