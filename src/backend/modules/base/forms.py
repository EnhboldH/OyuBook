from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm

from .models import (
    OyuUser,
    OyuUserProfile,
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

class UserProfileUpdateForm(ModelForm):

    class Meta:
        model = OyuUserProfile
        fields = ['fullname', 'region', 'facebook_link', 'insta_link', 'github_link', 'background_image', 'avatar_image']

    def __init__(self, request=None, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['fullname'].widget.attrs['class'] = "form-control login-input placeholder-no-fix"
        self.fields['region'].widget.attrs['class'] = "form-control login-input placeholder-no-fix"
        self.fields['region'].widget.attrs['placeholder'] = 'Enter your region'
        self.fields['fullname'].widget.attrs['placeholder'] = 'Enter your username'

    def clean(self):
        return self.cleaned_data
