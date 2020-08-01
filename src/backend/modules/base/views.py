from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import views
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q

from django.http import Http404
from django.http import HttpResponseRedirect

# Forms
from .forms import (
    UserRegistrationForm,
    UserProfileUpdateForm,
    LoginForm,
)

# Models
from .models import (
    OyuUser,
    OyuUserProfile,
)

class HomeView(View):
    context = {
        'title': 'Нүүр хуудас | OyuBook',
    }

    def get(self, request, *args, **kwargs):
        return render(request, 'home/index.html', self.context)

class PolicyView(View):
    context = { 
        'title': 'Нууцлалын бодлого | OyuBook',
    }

    def get(self, request, *args, **kwargs):
        return render(request, 'home/policy.html', self.context)

class SupportView(View):
    context = {
        'title': 'Биднийг дэмжих | OyuBook',
    }

    def get(self, request, *args, **kwargs):
        return render(request, 'home/support.html', self.context)

class UserCreateView(FormView):
    template_name = 'user/register.html'
    model = OyuUser
    form_class = UserRegistrationForm
    success_url = '/user/login/'
    extra_context = {
        'title': 'Шинэ хаяг нээх| OyuBook'
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

            OyuUserProfile.objects.create(
                oyu_user=user,
                fullname=user.username,
            ).save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_index')
        return self.render_to_response(self.get_context_data())


class UserLoginView(views.LoginView):
    form_class = LoginForm
    template_name = 'user/login.html'
    redirect_authenticated_user = True
    extra_context = {
        'title': 'Нэвтрэх | OyuBook'
    }


class UserLogoutView(views.LogoutView):
    pass

class UserProfileView(DetailView):
    model = OyuUser
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['title'] = obj.username
        context['profile'] = self.get_profile_data(oyu_user=obj)
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

    def get_profile_data(self, oyu_user):

        profile = OyuUserProfile.objects.filter(oyu_user=oyu_user).first()
        if not profile:
            return {}
        return profile


class UserProfileUpdateView(FormView):
    template_name = 'user/profile-update.html'
    form_class = UserProfileUpdateForm

    def view_prepare(self, request, *args, **kwargs):
        oyu_user = OyuUser.objects.filter(slug=self.kwargs.get('slug', None)).first()
        user_profile = OyuUserProfile.objects.filter(oyu_user=oyu_user).first()
        if not oyu_user or not user_profile:
            raise Http404("Хэрэглэгч олдсонгүй.")
        self.object = oyu_user
        self.user_profile = user_profile

    def get(self, request, *args, **kwargs):
        self.view_prepare(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.view_prepare(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.object
        context['title'] = self.object.username
        return context

    def get_initial(self):
        return {
            'fullname': self.user_profile.fullname,
            'region': self.user_profile.region,
            'email': self.object.email,
            'github_link': self.user_profile.github_link,
            'facebook_link': self.user_profile.facebook_link,
            'insta_link': self.user_profile.insta_link,
        }

    def form_valid(self, form):
        valid_data = form.cleaned_data
        oyu_user = self.request.user
        if valid_data.get('background_image', None) != None:
            oyu_user.background_image = valid_data.get('background_image', None)
        if valid_data.get('avatar_image', None) != None:
            oyu_user.avatar_image = valid_data.get('avatar_image', None)
        oyu_user.save()

        user_profile = OyuUserProfile.objects.filter(oyu_user=oyu_user).first()
        if user_profile:
            user_profile.fullname = valid_data.get('fullname', None)
            user_profile.region = valid_data.get('region', None)
            user_profile.facebook_link = valid_data.get('facebook_link', None)
            user_profile.insta_link = valid_data.get('insta_link', None)
            user_profile.github_link = valid_data.get('github_link', None)
            user_profile.save()

        return HttpResponseRedirect(reverse('user_profile', kwargs={'slug': self.object.slug}))
