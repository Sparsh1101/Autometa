from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import *
from django.conf import settings


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)