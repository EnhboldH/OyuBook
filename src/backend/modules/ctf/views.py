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
from django.contrib.sessions.models import Session
from django.utils import timezone

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
    def __init__(self):
        self.context = {
            'title': 'Нүүр Хуудас | Capture The Flag',
            'active_users': self.get_current_users(),
        }

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            self.context['profile'] = self.get_profile_data(oyu_user=user)
            if user.user_type == 'admin':
                self.context['challenge_request_count'] = CtfChallengeRequest.objects.count()
                self.context['challenge_count'] = CtfChallenge.objects.count()

        return render(request, 'ctf/index.html', self.context)

    def post(self, request, *args, **kwargs):
        return render(request, 'ctf/index.html', self.context)

    def get_profile_data(self, oyu_user):
        user_profile = OyuUserProfile.objects.filter(oyu_user=oyu_user).first()
        if not user_profile: return {}
        return user_profile

    def get_current_users(self):
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        user_id_list = []
        for session in active_sessions:
            data = session.get_decoded()
            user_id_list.append(data.get('_auth_user_id', None))
        return OyuUser.objects.filter(id__in=user_id_list)


class CTFChallengesView(View):
    context = {
        'title': 'Бодлогууд | Capture The Flag',
    }

    def get(self, request, *args, **kwargs):
        self.prepare_context()
        return render(request, 'ctf/challenges.html', self.context)

    def post(self, request, *args, **kwargs):
        user = request.user
        value = request.POST[list(request.POST)[1]]
        chall_id = list(request.POST)[1].split('-')[1]
        challenge = CtfChallenge.objects.filter(reference_id=chall_id).first()
        if challenge.flag == value:
            can_fb = False
            if user.is_authenticated:
                user_challenge = UserChallenge.objects.filter(oyu_user=user, challenge=challenge).first()
                user_profile = OyuUserProfile.objects.filter(oyu_user=user).first()
                if challenge.solved_users_count == 0: can_fb = True

                if user_challenge:
                    if user_challenge.status == 'solved':
                        self.prepare_context()
                        messages.error(request, 'Та аль хэдийн бодсон байна')
                        return render(request, 'ctf/challenges.html', self.context)

                    else:
                        user_challenge.status = 'solved'
                        user_challenge.save()

                else:
                    UserChallenge.objects.create(
                        oyu_user=user,
                        challenge=challenge,
                        status='solved',
                    ).save()

                if can_fb: user_profile.first_blood += 1
                user_profile.solved_problem += 1
                user_profile.score += challenge.value
                user_profile.save()
 
                challenge.solved_users_count += 1
                challenge.value = max(challenge.value - 5, 100)
                challenge.save()
            messages.success(request, 'Хариулт зөв байна')
        else:
            messages.error(request, 'Хариулт буруу байна')
            if user.is_authenticated:
                user_profile = OyuUserProfile.objects.filter(oyu_user=user).first()
                UserChallenge.objects.create(
                    oyu_user=request.user,
                    challenge=challenge,
                    status='attempted',
                ).save()
                user_profile.score = max(user_profile.score - 100, 0)
                user_profile.save()
        self.prepare_context()
        return render(request, 'ctf/challenges.html', self.context)

    def prepare_context(self):
        user = self.request.user
        
        author_clist = []
        solved_clist = []
        attempt_clist = []
        unsolved_clist = []

        if user.is_authenticated:
            for cll in CtfChallenge.objects.all():
                data = {
                    'title': cll.title,
                    'category': cll.category,
                    'value': cll.value,
                    'solved_users_count': cll.solved_users_count,
                    'description': cll.description,
                    'author': cll.author,
                    'hid': cll.reference_id,
                }
                print(cll)
                if cll.author.username == user.username:
                    print('auth')
                    author_clist.append(data)
                elif UserChallenge.objects.filter(oyu_user=user, challenge=cll, status='solved').first():
                    print('solved')
                    solved_clist.append(data)
                elif UserChallenge.objects.filter(oyu_user=user, challenge=cll, status='attempted').first():
                    print('att')
                    attempt_clist.append(data)
                else:
                    print('unsolv')
                    unsolved_clist.append(data)

            self.context['author_clist'] = author_clist
            self.context['solved_clist'] = solved_clist
            self.context['attempt_clist'] = attempt_clist
            self.context['unsolved_clist'] = unsolved_clist
        else:
            self.context['challenges'] = CtfChallenge.objects.all()
        self.context['tops'] = OyuUserProfile.objects.order_by('-score')[:5]

class CTFChallengeRequestView(FormView):
    template_name = 'ctf/challenge-request.html'
    model = CtfChallengeRequest
    form_class = CTFChallengeRequestForm
    success_url = '/ctf/challenge/request'
    extra_context = {
        'title': 'Бодлого нэмэх | Capture The Flag',
    }

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            messages.info(request, 'Бодлого нэмэхийн тулд та нэвтэрнэ үү')
            return redirect('user_login')
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        user = self.request.user
        challenge_data = form.cleaned_data

        if user.user_type == 'admin':

            CtfChallenge.objects.create(
                title=challenge_data.get('title'),
                description=challenge_data.get('description'),
                category=challenge_data.get('category'),
                flag=challenge_data.get('flag'),
                author=user,
            ).save()
            # Adding `reference_id`
            ctf_chall = CtfChallenge.objects.last()
            ctf_chall.reference_id = ctf_chall.id
            ctf_chall.save()

            user_profile = OyuUserProfile.objects.filter(oyu_user=user).first()
            user_profile.accepted_problem += 1
            user_profile.save()

            messages.success(self.request, 'Бодлого амжилттай нэмлээ')
            return super().form_valid(form)

        challenge_request = CtfChallengeRequest()
        challenge_request.title = challenge_data.get('title')
        challenge_request.description = challenge_data.get('description')
        challenge_request.category = challenge_data.get('category')
        challenge_request.solution = challenge_data.get('solution')
        challenge_request.flag = challenge_data.get('flag')
        challenge_request.oyu_user = user
        challenge_request.save()
        messages.success(self.request, 'Бид таны бодлогыг шалгаж үзээд таньд мэдэгдэх болно')

        return super().form_valid(form)


class CTFScoreboardView(View):
    context = {
        'title': 'Онооны самбар | Capture The Flag',
    }

    def get(self, request, *args, **kwargs):
        self.context['users'] = OyuUserProfile.objects.order_by('-score')
        return render(request, 'ctf/scoreboard.html', self.context)

# Admin views

class CTFAdminChallengeRequestsView(View):
    context = {
        'title': 'Админ бодлогын хүсэлтүүд | Capture The Flag',
    }

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated or user.user_type != 'admin':
            return redirect('home_index')
        self.context['challenges'] = CtfChallengeRequest.objects.all()
        return render(request, 'ctf/admin/admin-challenge-requests.html', self.context)

    def post(self, request, *args, **kwargs):
        action, challenge_id = request.POST['challenge'].split('-')
        if action == 'delete':
            challenge = CtfChallengeRequest.objects.get(pk=challenge_id).delete()
            messages.success(request, 'Бодлого амжилттай устгагдлаа')
            self.context['challenges'] = CtfChallengeRequest.objects.all()
            return render(request, 'ctf/admin/admin-challenge-requests.html', self.context)

        challenge = CtfChallengeRequest.objects.get(pk=challenge_id)
        req_user = challenge.oyu_user
        CtfChallenge.objects.create(
            title=challenge.title,
            description=challenge.description,
            category=challenge.category,
            flag=challenge.flag,
            author=req_user,
        ).save()
        ctf_chall = CtfChallenge.objects.last()
        ctf_chall.reference_id = ctf_chall.id
        ctf_chall.save()

        challenge.delete()
        ctf_chall = CtfChallenge.objects.last()
        UserChallenge.objects.create(
            oyu_user=req_user,
            challenge=ctf_chall,
        ).save()
        user_profile = OyuUserProfile.objects.filter(oyu_user=req_user).first()
        user_profile.accepted_problem += 1
        user_profile.save()

        self.context['challenges'] = CtfChallengeRequest.objects.all()
        messages.success(request, 'Бодлого амжилттай нэмлээ')
        return render(request, 'ctf/admin/admin-challenge-requests.html', self.context)


class CTFAdminChallengesView(View):
    context = {
        'title': 'Нийт бодлогууд | Capture The Flag',
    }

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated or user.user_type != 'admin':
            return redirect('home_index')
        self.context['challenges'] = CtfChallenge.objects.all()
        return render(request, 'ctf/admin/admin-challenges.html', self.context)

    def post(self, request, *args, **kwargs):
        challenge_id = request.POST['challenge']
        challenge = CtfChallenge.objects.get(pk=challenge_id).delete()
        messages.success(request, 'Бодлого амжилттай устгагдлаа')
        self.context['challenges'] = CtfChallenge.objects.all()
        return render(request, 'ctf/admin/admin-challenges.html', self.context)
