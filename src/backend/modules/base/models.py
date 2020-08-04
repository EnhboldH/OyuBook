import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

from modules.base.consts import (
    USER_TYPE_NORMAL,
    USER_TYPE_CHOICES,
    USER_CHALLENGE_STATUS_CHOICES,
    USER_CHALLENGE_STATUS_UNSOLVED,
    USER_BADGE_TYPE_CHOICES,
    USER_BADGE_TYPE_NORMAL,
    USER_REGION_CHOICES,
    CTF_CHALLENGE_CATEGORY_CHOICES,
    BACKGROUND_IMG_DEFAULT,
    AVATAR_IMG_DEFAULT
)

from django.template.defaultfilters import slugify

from django.urls import reverse
from martor.models import MartorField
from hashid_field import HashidField

class OyuUser(AbstractUser, models.Model):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    user_type = models.CharField(max_length=100, default=USER_TYPE_NORMAL, choices=USER_TYPE_CHOICES)
    slug = models.SlugField(null=False, unique=True)

    background_image = models.ImageField("Background Img", max_length=128, default=BACKGROUND_IMG_DEFAULT, upload_to='img/users/background', null=True)
    avatar_image = models.ImageField("Avatar Img", max_length=128, default=AVATAR_IMG_DEFAULT, upload_to='img/users/avatar', null=True)

    created_date = models.DateField(auto_now_add=True)
    last_updated_date = models.DateField(auto_now=True)

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


class OyuUserProfile(models.Model):
    REQUIRED_FIELDS = ["oyu_user"]

    oyu_user = models.ForeignKey(OyuUser, verbose_name="Oyu User", on_delete=models.CASCADE)
    fullname = models.CharField("Бүтэн нэр", max_length=20, null=True, blank=True)
    region = models.CharField("Харьяа", max_length=100, blank=True, null=True, choices=USER_REGION_CHOICES, help_text="Сургууль эсвэл ажилладаг газар.")
    respected = models.PositiveIntegerField("Хүндлэгдсэн", default=0, null=True)
    solved_problem = models.PositiveIntegerField("Бодсон бодлогын тоо", default=0, null=True)
    score = models.PositiveIntegerField("Цуглуулсан оноо", default=0, null=True)
    badge_type = models.CharField("Цол", max_length=50, choices=USER_BADGE_TYPE_CHOICES, default=USER_BADGE_TYPE_NORMAL, null=True)
    first_blood = models.PositiveIntegerField("Түрүүлж бодсон", default=0, null=True)
    accepted_problem = models.PositiveIntegerField("Оруулсан бодлогын тоо", default=0, null=True)
    given_money = models.PositiveIntegerField("Хандив", default=0, null=True)

    facebook_link = models.CharField("Facebook link", max_length=128, blank=True, null=True)
    insta_link = models.CharField("Insta link", max_length=128, blank=True, null=True)
    github_link = models.CharField("Github link", max_length=128, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.oyu_user.__str__()

    def save(self, *args, **kwargs):
        self.last_updated_date = datetime.datetime.now()
        super(OyuUserProfile, self).save(*args, **kwargs)


class CtfChallenge(models.Model):
    REQUIRED_FIELDS = ['oyu_user']

    # General
    title = models.CharField("Гарчиг", max_length=30, unique=True)
    author = models.ForeignKey(OyuUser, verbose_name='Нэмсэн', on_delete=models.DO_NOTHING, null=True)
    description = MartorField()
    value = models.PositiveIntegerField("Бодлогын оноо", default=500, null=True)
    category = models.CharField("Төрөл", max_length=100, choices=CTF_CHALLENGE_CATEGORY_CHOICES, null=True)
    state = models.CharField("Төлөв", max_length=100, null=True, default='active')
    flag = models.CharField("Flag", max_length=100, null=False)

    # Additional
    solved_users_count = models.PositiveIntegerField("Бодсон хэрэглэгчдийн тоо", null=True, default=0)

    # Security
    reference_id = HashidField(allow_int_lookup=True, null=True, salt='CHANGEMEINFUTURE', min_length=15)

    def __str__(self):
        return "%s | %s" % (self.title, self.category)


class CtfChallengeRequest(models.Model):
    title = models.CharField("Гарчиг", max_length=30, unique=True)
    oyu_user = models.ForeignKey(OyuUser, verbose_name="Хэрэглэгч", on_delete=models.DO_NOTHING)
    description = MartorField()
    category = models.CharField("Төрөл", choices=CTF_CHALLENGE_CATEGORY_CHOICES, max_length=100)
    solution = models.CharField("Хэрхэн бодох", max_length=300)
    flag = models.CharField("Flag", max_length=100)

    def __str__(self):
        return "%s | %s" % (self.oyu_user.__str__(), self.title)

class UserChallenge(models.Model):
    REQUIRED_FIELDS = ["oyu_user", "challenge"]

    oyu_user = models.ForeignKey(OyuUser, verbose_name="Хэрэглэгч", on_delete=models.DO_NOTHING)
    challenge = models.ForeignKey(CtfChallenge, verbose_name="Challenge", on_delete=models.CASCADE)

    status = models.CharField("Төлөв", max_length=100, choices=USER_CHALLENGE_STATUS_CHOICES, default=USER_CHALLENGE_STATUS_UNSOLVED)

    def __str__(self):
        return "%s | %s" % (self.oyu_user.__str__(), self.challenge.__str__())
