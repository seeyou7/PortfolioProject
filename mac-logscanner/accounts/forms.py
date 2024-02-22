from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()  # Adding an email field to the form

    class Meta:
        model = User  # Specifying the model with which the form interacts
        fields = ['username', 'email', 'password1', 'password2']  # Fields to include in the form
