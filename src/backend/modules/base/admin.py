from django.db import models
from django.contrib import admin

from martor.widgets import AdminMartorWidget
from martor.models import MartorField

from .models import (
    OyuUser,
    CtfChallenge,
    CtfChallengeRequest,
    OyuUserProfile,
)


class CtfChallengeRequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'id']
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

admin.site.register(OyuUser)
admin.site.register(CtfChallenge)
admin.site.register(OyuUserProfile)
admin.site.register(CtfChallengeRequest, CtfChallengeRequestAdmin)