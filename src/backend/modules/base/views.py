from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth import views
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
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
        'title': 'Нүүр хуудас | OyuBook',
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

class UserLogoutView(views.LogoutView):
    next_page = '/'
    extra_context = {
        'title': 'Гарах | OyuBook'
    }

class UserProfileView(DetailView):
    model = OyuUser
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['title'] = obj.username
        return context

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})
        if pk is None and slug is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj