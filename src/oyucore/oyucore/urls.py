from django.contrib import admin
from django.urls import path

from modules.base.views import HomeView
from modules.base.views import UserLoginView
from modules.base.views import FrontLogoutView
from modules.base.views import UserCreateView
from modules.base.views import UserBlaBlaView

from modules.ctf.views import ctf_index
from modules.mathematics.views import math_index
from modules.electronics.views import elec_index
from modules.network.views import network_index


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('user/login/', UserLoginView.as_view(), name='user_login'),
    path('user/logout/', FrontLogoutView.as_view(), name='user_logout'),
    path('user/register/', UserCreateView.as_view(), name='user_register'),
    path('user/mdkue/', UserBlaBlaView.as_view(), name='user_mdkue'),
    path('ctf/', ctf_index, name='ctf_index'),
    path('mathematics/', math_index, name='mathematics_index'),
    path('electronics/', elec_index, name='electronics_index'),
    path('network/', network_index, name='network_index'),
]
