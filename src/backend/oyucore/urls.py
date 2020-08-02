from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from modules.base.views import (
    HomeView,
    PolicyView,
    SupportView,
    UserLoginView,
    UserLogoutView,
    UserCreateView,
    UserProfileView,
    UserProfileUpdateView,
)
from modules.ctf.views import (
    CTFHomeView,
    CTFChallengesView,
    CTFChallengeRequestView,
    CTFScoreboardView,
    CTFAdminChallengeRequestsView,
    CTFAdminChallengesView,
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
    # Base module
    path('', HomeView.as_view(), name='home_index'),
    path('privacy-policy/', PolicyView.as_view(), name='home_policy'),
    path('support/', SupportView.as_view(), name='home_support'),
    path('user/login/', UserLoginView.as_view(), name='user_login'),
    path('user/logout/', UserLogoutView.as_view(), name='user_logout'),
    path('user/register/', UserCreateView.as_view(), name='user_register'),
    path('user/profile/<slug:slug>', UserProfileView.as_view(), name='user_profile'),
    path('user/profile/update/<slug:slug>/', UserProfileUpdateView.as_view(), name='user_profile_update'),
    # CTF module
    path('ctf/', CTFHomeView.as_view(), name='ctf_index'),
    path('ctf/scoreboard', CTFScoreboardView.as_view(), name='ctf_scoreboard'),
    path('ctf/challenges/', CTFChallengesView.as_view(), name='ctf_challenges'),
    path('ctf/challenge/request/', CTFChallengeRequestView.as_view(), name='ctf_challenge_request'),
    path('ctf/admin/challenge/requests/', CTFAdminChallengeRequestsView.as_view(), name='ctf_admin_challenge_requests'),
    path('ctf/admin/challenges/', CTFAdminChallengesView.as_view(), name='ctf_admin_challenges'),
    # Mathematics module
    path('mathematics/', MathematicsView.as_view(), name='mathematics_index'),
    # Electronics module
    path('electronics/', ElectronicsView.as_view(), name='electronics_index'),
    # Network module
    path('network/', NetworkView.as_view(), name='network_index'),

    # Third part module
    path('martor/', include('martor.urls')), # Don't delete this if you don't know
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()