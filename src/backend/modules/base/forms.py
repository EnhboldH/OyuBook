from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm

from .models import (
    OyuUser,
    OyuUserProfile,
    CtfChallengeRequest,
)

from .consts import (
    USER_REGION_CHOICES,
    CTF_CHALLENGE_CATEGORY_CHOICES,
)
# Third party
from martor.fields import MartorFormField

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
                'required': 'И-мэйл оруулна уу',
                'unique': 'И-мэйл давхардаж байна',
            },
        }

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'autofocus': 'autofocus'})
        self.fields['username'].widget.attrs['placeholder'] = u"Бүртгүүлэх нэр"
        self.fields['email'].widget.attrs['placeholder'] = u"И-мэйл хаяг"
        self.fields['password'].widget.attrs['placeholder'] = u"Нууц үг"

        for vis in self.visible_fields(): vis.field.widget.attrs['class'] = 'form-control _input'


class LoginForm(AuthenticationForm):

    username = forms.EmailField(label="Е-мэйл хаяг", max_length=100, required=True)

    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': ''})
        for vis in self.visible_fields(): 
            vis.field.widget.attrs['class'] = 'form-control _input'

        self.fields['username'].widget.attrs['placeholder'] = u'И-мэйл хаяг'
        self.fields['password'].widget.attrs['placeholder'] = u'Нууц үг'


    def clean_username(self, ):
        uname = self.cleaned_data.get("username")
        if uname: uname = uname.strip()
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
            self.fields[field].widget.attrs['class'] = 'form-control _input'
            self.fields[field].widget.attrs['placeholder'] = '. . .'

        self.fields['avatar_image'].widget.attrs['class'] = "form-control-file"
        self.fields['background_image'].widget.attrs['class'] = "form-control-file"

    def clean(self):
        return self.cleaned_data

class CTFChallengeRequestForm(ModelForm):
    class Meta:
        model = CtfChallengeRequest
        fields = ['title', 'description', 'category', 'solution', 'flag']

    def __init__(self, request=None, *args, **kwargs):
        super(CTFChallengeRequestForm, self).__init__(*args, **kwargs)

        for field in self.fields: self.fields[field].widget.attrs['class'] = 'form-control _input'

        self.fields['title'].widget.attrs['placeholder'] = u"Бодлогын нэрийг оруулна уу"
        self.fields['solution'].widget.attrs['placeholder'] = u"Бид таны бодлогыг шалгахын тулд заавал бөглөнө үү"
        self.fields['flag'].widget.attrs['placeholder'] = u"Хариу буюу флагаа оруулна уу"
