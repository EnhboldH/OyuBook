from django.contrib import admin
from django.urls import path

from modules.base.views import (
    HomeView,
    UserLoginView,
    UserLogoutView,
    UserCreateView,
    UserProfileView,
)
from modules.ctf.views import (
    CTFHomeView
)
from modules.mathematics.views import math_index
from modules.electronics.views import elec_index
from modules.network.views import network_index


urlpatterns = [
    path('admin/', admin.site.urls),
    # Home 
    path('', HomeView.as_view(), name='home_index'),
    # Users
    path('user/login/', UserLoginView.as_view(), name='user_login'),
    path('user/logout/', UserLogoutView.as_view(), name='user_logout'),
    path('user/register/', UserCreateView.as_view(), name='user_register'),
    path('user/profile/<slug:slug>', UserProfileView.as_view(), name='user_profile'),
    # CTF
    path('ctf/', CTFHomeView.as_view(), name='ctf_index'),
    # Mathematics
    path('mathematics/', math_index, name='mathematics_index'),
    # Electronics
    path('electronics/', elec_index, name='electronics_index'),
    # Network
    path('network/', network_index, name='network_index'),
]