import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

from modules.base.consts import USER_TYPE_NORMAL
from modules.base.consts import USER_TYPE_CHOICES
from modules.base.consts import USER_CHALLENGE_STATUS_CHOICES
from modules.base.consts import USER_CHALLENGE_STATUS_ATTEMPTED
from modules.base.consts import USER_BADGE_TYPE_CHOICES
from modules.base.consts import USER_BADGE_TYPE_NORMAL
from modules.base.consts import USER_REGION_CHOICES
from modules.base.consts import CTF_CHALLENGE_CATEGORY_CHOICES
from modules.base.consts import BACKGROUND_IMG_DEFAULT
from modules.base.consts import AVATAR_IMG_DEFAULT

from django.template.defaultfilters import slugify

from django.urls import reverse


class OyuUser(AbstractUser, models.Model):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    user_type = models.CharField(max_length=100, default=USER_TYPE_NORMAL, choices=USER_TYPE_CHOICES)
    slug = models.SlugField(null=False, unique=True)

    background_image = models.ImageField("Background Img", max_length=128, default=BACKGROUND_IMG_DEFAULT, upload_to='img/users/background')
    avatar_image = models.ImageField("Avatar Img", max_length=128, default=AVATAR_IMG_DEFAULT, upload_to='img/users/avatar')

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


class OyuUserProfile(models.Model):
    REQUIRED_FIELDS = ["oyu_user"]

    oyu_user = models.ForeignKey(OyuUser, verbose_name="Oyu User", on_delete=models.CASCADE)
    fullname = models.CharField("Бүтэн нэр", max_length=20)
    region = models.CharField("Харьяа", max_length=100, blank=True, null=True, choices=USER_REGION_CHOICES, help_text="Сургууль эсвэл ажилладаг газар.")
    respected = models.PositiveIntegerField("Хүндлэгдсэн", default=0)
    solved_problem = models.PositiveIntegerField("Бодсон бодлогын тоо", default=0)
    score = models.PositiveIntegerField("Цуглуулсан оноо", default=0)
    badge_type = models.CharField("Цол", max_length=50, choices=USER_BADGE_TYPE_CHOICES, default=USER_BADGE_TYPE_NORMAL)
    first_blood = models.PositiveIntegerField("Түрүүлж бодсон", default=0)
    accepted_problem = models.PositiveIntegerField("Оруулсан бодлогын тоо", default=0)
    given_money = models.PositiveIntegerField("Хандив", default=0)

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
    title = models.CharField("Гарчиг", max_length=100, unique=True)
    description = models.TextField("Бодлогын өгүүлбэр", max_length=10000)
    value = models.PositiveIntegerField("Бодлогын оноо", default=0)
    category = models.CharField("Төрөл", max_length=100, choices=CTF_CHALLENGE_CATEGORY_CHOICES, null=True)
    state = models.CharField("Төлөв", max_length=100, null=True, default='active')
    flag = models.CharField("Flag", max_length=100, null=False)
    solved_users_count = models.PositiveIntegerField("Бодсон хэрэглэгчдийн тоо", null=True, default=0)

    def __str__(self):
        return "%s | %s" % (self.title, self.category)

class UserChallenge(models.Model):
    REQUIRED_FIELDS = ["oyu_user", "challenge"]

    oyu_user = models.ForeignKey(OyuUser, verbose_name="Хэрэглэгч", on_delete=models.DO_NOTHING)
    challenge = models.ForeignKey(CtfChallenge, verbose_name="Challenge", on_delete=models.DO_NOTHING)
    status = models.CharField("Төлөв", max_length=100, choices=USER_CHALLENGE_STATUS_CHOICES, default=USER_CHALLENGE_STATUS_ATTEMPTED)

    def __str__(self):
        return "%s | %s" % (self.oyu_user.__str__(), self.challenge.__str__())
