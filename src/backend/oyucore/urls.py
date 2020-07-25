from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from modules.base.views import (
    HomeView,
    UserLoginView,
    UserLogoutView,
    UserCreateView,
    UserProfileView,
    UserProfileUpdateView,
)
from modules.ctf.views import (
    CTFHomeView,
    CTFChallengesView,
    CTFChallengeAdd,
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

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Home 
    path('', HomeView.as_view(), name='home_index'),
    # Users
    path('user/login/', UserLoginView.as_view(), name='user_login'),
    path('user/logout/', UserLogoutView.as_view(), name='user_logout'),
    path('user/register/', UserCreateView.as_view(), name='user_register'),
    path('user/profile/<slug:slug>', UserProfileView.as_view(), name='user_profile'),
    path('user/profile/update/<slug:slug>/', UserProfileUpdateView.as_view(), name='user_profile_update'),
    # CTF
    path('ctf/', CTFHomeView.as_view(), name='ctf_index'),
    path('ctf/challenges/', CTFChallengesView.as_view(), name='ctf-challenges'),
    path('ctf/challenges/add/', CTFChallengeAdd.as_view(), name='ctf-addchallenge'),
    # Mathematics
    path('mathematics/', MathematicsView.as_view(), name='mathematics_index'),
    # Electronics
    path('electronics/', ElectronicsView.as_view(), name='electronics_index'),
    # Network
    path('network/', NetworkView.as_view(), name='network_index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()