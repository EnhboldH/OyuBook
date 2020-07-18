from django.contrib import admin
from .models import (
    OyuUser,
    CtfChallenge,
    OyuUserProfile
)

admin.site.register(OyuUser)
admin.site.register(CtfChallenge)
admin.site.register(OyuUserProfile)
