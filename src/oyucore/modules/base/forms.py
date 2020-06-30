from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm

from .models import (
    OyuUser
)

class UserRegistrationForm(ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = OyuUser
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'autofocus': 'autofocus'})

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control login-input'


class LoginForm(AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = "form-control placeholder-no-fix"
        self.fields['password'].widget.attrs['class'] = "form-control placeholder-no-fix"
        self.fields['username'].widget.attrs['placeholder'] = u"Имэйл хаяг"
        self.fields['password'].widget.attrs['placeholder'] = u"Нууц үг"

    def clean_username(self, ):
        uname = self.cleaned_data.get("username")
        if uname:
            uname = uname.strip()
        return uname
