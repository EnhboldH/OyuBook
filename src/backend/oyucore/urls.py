from django.contrib import admin
from django.urls import path

from modules.base.views import (
    HomeView,
    UserLoginView,
    UserLogoutView,
    UserCreateView,
    UserProfileView,
    UserProfileEditView,
)
from modules.ctf.views import (
    CTFHomeView
)
from modules.mathematics.views import (
    MathematicsView
)
from modules.electronics.views import (
    ElectronicsView
)
from modules.network.views import (
    NetworkView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # Home 
    path('', HomeView.as_view(), name='home_index'),
    # Users
    path('user/login/', UserLoginView.as_view(), name='user_login'),
    path('user/logout/', UserLogoutView.as_view(), name='user_logout'),
    path('user/register/', UserCreateView.as_view(), name='user_register'),
    path('user/profile/<slug:slug>', UserProfileView.as_view(), name='user_profile'),
    path('user/profile/<slug:slug>/update/', UserProfileEditView.as_view(), name='user_profile_update'),
    # CTF
    path('ctf/', CTFHomeView.as_view(), name='ctf_index'),
    # Mathematics
    path('mathematics/', MathematicsView.as_view(), name='mathematics_index'),
    # Electronics
    path('electronics/', ElectronicsView.as_view(), name='electronics_index'),
    # Network
    path('network/', NetworkView.as_view(), name='network_index'),
]