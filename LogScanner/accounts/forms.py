#form modul contains cls method pour cree html form
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User # to represent user in db

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        #class to hold config for the parent class UserCF follow by cls attr
        model = User
        fields = ['username', 'email', 'password1', 'password2']