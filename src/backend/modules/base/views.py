from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth import views
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.db.models import Q

# Forms
from .forms import (
    UserRegistrationForm,
    LoginForm
)

# Models
from .models import OyuUser


class HomeView(View):
    context = {
        'title': 'Нүүр хуудас | OyuBook',
    }

    def get(self, request, *args, **kwargs):
        return render(request, 'home/index.html', self.context)


class UserCreateView(UserPassesTestMixin, FormView):
    template_name = 'users/register.html'
    model = OyuUser
    form_class = UserRegistrationForm
    success_url = '/user/login/'
    extra_context = {
        'title': 'Бүртгүүлэх | OyuBook'
    }

    def form_valid(self, form):
        user_data = form.cleaned_data
        is_user_duplicated = OyuUser.objects.filter(
            Q(email__iexact=user_data.get('email')) |
            Q(username__iexact=user_data.get('username'))
        ).first()
        if not is_user_duplicated:
            # Хэрэглэгчийн мэдээлэл дээр тулгуурлан хэрэглэгч үүсгэе.
            user = OyuUser()
            user.email = user_data.get('email')
            user.username = user_data.get('username')
            user.set_password(user_data.get('password'))
            user.save()
        return super().form_valid(form)
        
    # Хэрэглэгч нэвтэрсэн үед /login хуудсыг дуудахгүй шууд /home дуудна
    # гэхдээ одоогийн байдлаар 403 өгнө
    def test_func(self):
        if self.request.user.is_authenticated:
            return False
        else:
            return True

class UserLoginView(UserPassesTestMixin, views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Нэвтрэх | OyuBook'
    }

    def get_success_url(self):
        return reverse('home_index')

    # Хэрэглэгч нэвтэрсэн үед /login хуудсыг дуудахгүй шууд /home дуудна
    # гэхдээ одоогийн байдлаар 403 өгнө
    def test_func(self):
        if self.request.user.is_authenticated:
            return False
        else:
            return True

class UserLogoutView(views.LogoutView):
    next_page = '/'
    extra_context = {
        'title': 'Гарах | OyuBook'
    }

class UserProfileView(DetailView):
    model = OyuUser
    template_name = 'users/profile.html'
    extra_context = {
        'title': 'Хэрэглэгч'
    }
