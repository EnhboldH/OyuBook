from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth import views
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

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
        'title': 'OyuBook - Нүүр хуудас',
    }

    def get(self, request, *args, **kwargs):
        return render(request, 'home/index.html', self.context)


class UserCreateView(FormView):
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


class UserLoginView(views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Нэвтрэх | OyuBook'
    }

    def get_success_url(self):
        return reverse('home-index')


class UserLogoutView(views.LogoutView):
    next_page = '/'
    extra_context = {
        'title': 'Гарах | OyuBook'
    }

class UserBlaBlaView(LoginRequiredMixin, TemplateView):

    template_name = "users/mdkue.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Mdkueshdee yu iin ene"
        print (self.request.user)
        context['current_user'] = self.request.user
        return context
