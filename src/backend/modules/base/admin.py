from django.contrib import admin
from .models import (
    OyuUser,
    CtfChallenge,
)

admin.site.register(OyuUser)
admin.site.register(CtfChallenge)