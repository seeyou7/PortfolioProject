from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        #class to hold config for the parent class UserCF 
        model = User
        fields = ['username', 'email', 'password1', 'password2']