from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *
from shared.encryption import EncryptionHelper

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "GET":
        form = UserInfoForm()
        user_creation_form = UserCreationForm()
        return render(
            request,
            "register.html",
            {
                "form": form,
                "user_creation_form": user_creation_form,
            },
        )
    else:
        form = UserInfoForm(request.POST)
        user_creation_form = UserCreationForm(request.POST)
        Ruser = user_creation_form.save(commit=False)
        Ruser.save()

        Suser = form.save(commit=False)
        Suser.user = Ruser
        Suser.fname = encryptionHelper.encrypt(request.POST["fname"])
        Suser.lname = encryptionHelper.encrypt(request.POST["lname"])
        Suser.email = encryptionHelper.encrypt(request.POST["email"])
        Suser.aadhar = encryptionHelper.encrypt(request.POST["aadhar"])
        Suser.dob = encryptionHelper.encrypt(Suser_dob)
        Suser.mobile_no = encryptionHelper.encrypt(request.POST["mobile_no"])
        Suser.gender = encryptionHelper.encrypt(request.POST["gender"])
        Suser.save()
        return redirect("registration:loggedIn")

def loggedIn(request):
    return render(request, 'loggedIn.html')

def login(request):
    return render(request, 'login.html')