import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

from modules.base.consts import USER_TYPE_NORMAL
from modules.base.consts import USER_TYPE_CHOICES

from django.template.defaultfilters import slugify

from django.urls import reverse

class OyuUser(AbstractUser, models.Model):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    image_file = models.CharField(max_length=100, default='default.jpg')
    user_type = models.CharField(max_length=100, default=USER_TYPE_NORMAL, choices=USER_TYPE_CHOICES)
    slug = models.SlugField(null=False, unique=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "OyuUser"

    def __str__(self):
        return "%s | %s" % (self.username, self.email)

    def __unicode(self):
        return "%s | %s" % (self.username, self.email)

    def save(self, *args, **kwargs):
        self.last_updated_date = datetime.datetime.now()
        if not self.slug:
            self.slug = slugify(self.username)

        return super(OyuUser, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'slug': self.slug})