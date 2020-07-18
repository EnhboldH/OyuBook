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

    """
    Энэ дээр mail ээр нэвтрээд зөв ажиллаад байгаа мөртлөө username field
    ашиглаад HTML дээр username хийнэ гэж харагдаж байна.
    Fix: username -> mail 
    """
    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = "form-control login-input placeholder-no-fix"
        self.fields['password'].widget.attrs['class'] = "form-control login-input placeholder-no-fix"
        self.fields['username'].widget.attrs['placeholder'] = u"Е-мэйл хаяг"
        self.fields['password'].widget.attrs['placeholder'] = u"Нууц үг"

    def clean_username(self, ):
        uname = self.cleaned_data.get("username")
        if uname:
            uname = uname.strip()
        return uname

class UserProfileUpdateForm(ModelForm):
    pass