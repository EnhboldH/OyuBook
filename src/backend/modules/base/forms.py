from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from martor.fields import MartorFormField

from .models import (
    OyuUser,
    OyuUserProfile,
    CtfChallengeRequest,
)

from .consts import (
    USER_REGION_CHOICES,
    CTF_CHALLENGE_CATEGORY_CHOICES,
)
class UserRegistrationForm(ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = OyuUser
        fields = ['username', 'email', 'password']
        error_messages = {
            'username': {
                'required': 'Нэрээ оруулна уу',
                'unique': 'Нэр давхардаж байна',
            },
            'email': {
                'required': 'Е-мэйл оруулна уу',
                'unique': 'Е-мэйл давхардаж байна',
            },
        }

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'autofocus': 'autofocus'})
        self.fields['username'].widget.attrs['placeholder'] = u"Бүртгүүлэх нэр"
        self.fields['email'].widget.attrs['placeholder'] = u"Е-мэйл хаяг"
        self.fields['password'].widget.attrs['placeholder'] = u"Нууц үг"

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control login-input'


class LoginForm(AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = "form-control login-input placeholder-no-fix"
        self.fields['password'].widget.attrs['class'] = "form-control login-input placeholder-no-fix"
        self.fields['username'].widget.attrs['placeholder'] = u"Хэрэглэгчийн нэр"
        self.fields['password'].widget.attrs['placeholder'] = u"Нууц үг"

    def clean_username(self, ):
        uname = self.cleaned_data.get("username")
        if uname:
            uname = uname.strip()
        return uname

class UserProfileUpdateForm(forms.Form):

    email = forms.EmailField(label="Е-мэйл хаяг", max_length=100, required=False)
    password = forms.CharField(label="Нууц үг", widget=forms.PasswordInput, required=False)
    background_image = forms.ImageField(label="Арын зураг", max_length=128, required=False)
    avatar_image = forms.ImageField(label="Нүүр зураг", max_length=128, required=False)

    fullname = forms.CharField(label="Бүтэн нэр", max_length=20, required=False)
    region = forms.ChoiceField(label="Харьяа", choices=USER_REGION_CHOICES, help_text="Сургууль эсвэл ажилладаг газар.", required=False)
    facebook_link = forms.CharField(label="Facebook link", max_length=128, required=False)
    insta_link = forms.CharField(label="Insta link", max_length=128, required=False)
    github_link = forms.CharField(label="Github link", max_length=128, required=False)

    def __init__(self, request=None, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control profile-input"
            self.fields[field].widget.attrs['placeholder'] = ". . ."

        self.fields['avatar_image'].widget.attrs['class'] = "form-control-file"
        self.fields['background_image'].widget.attrs['class'] = "form-control-file"

    def clean(self):

        # print ("Raw Data:", self.data)
        # print ("Raw files:", self.files)
        return self.cleaned_data

class CTFChallengeRequestForm(ModelForm):
    class Meta:
        model = CtfChallengeRequest
        fields = ['title', 'description', 'category', 'solution', 'flag']

    def __init__(self, request=None, *args, **kwargs):
        super(CTFChallengeRequestForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control input'
