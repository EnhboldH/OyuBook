from django.contrib import admin
from django.urls import path

from modules.base.views import HomeView
from modules.base.views import UserLoginView
from modules.base.views import UserLogoutView
from modules.base.views import UserCreateView
from modules.base.views import UserBlaBlaView

from modules.ctf.views import ctf_index
from modules.mathematics.views import math_index
from modules.electronics.views import elec_index
from modules.network.views import network_index


urlpatterns = [
    path('admin/', admin.site.urls),
    # Home 
    path('', HomeView.as_view(), name='home-index'),
    # Users
    path('user/login/', UserLoginView.as_view(), name='user-login'),
    path('user/logout/', UserLogoutView.as_view(), name='user-logout'),
    path('user/register/', UserCreateView.as_view(), name='user-register'),
    path('user/mdkue/', UserBlaBlaView.as_view(), name='user-mdkue'),
    # CTF
    path('ctf/', ctf_index, name='ctf-index'),
    # Mathematics
    path('mathematics/', math_index, name='mathematics-index'),
    # Electronics
    path('electronics/', elec_index, name='electronics-index'),
    # Network
    path('network/', network_index, name='network-index'),
]
