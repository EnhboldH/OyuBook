from django.shortcuts import render
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

    def get_context_data(self, *args, **kwargs):
        data = super(UserCreateView, self).get_context_data(*args, **kwargs)
        data['title'] = 'Бүртгүүлэх | OyuBook'
        return data

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
    # Одоохондоо Session байхгүй ч ингэсгээд үлдээлээ.
    form_class = LoginForm
    template_name = 'users/login.html'


class FrontLogoutView(views.LogoutView):
    template_name = 'users/logout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "You kicked out."
        return context


class UserBlaBlaView(LoginRequiredMixin, TemplateView):

    template_name = "users/mdkue.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Mdkueshdee yu iin ene"
        print (self.request.user)
        context['current_user'] = self.request.user
        return context
