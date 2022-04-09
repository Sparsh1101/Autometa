from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *

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
        if form.is_valid() and user_creation_form.is_valid():
            Ruser = user_creation_form.save(commit=False)
            Ruser.save()

            Suser = form.save(commit=False)
            Suser.user = Ruser
            Suser.fname = request.POST["fname"]
            Suser.lname = request.POST["lname"]
            Suser.email = request.POST["email"]
            Suser.aadhar = request.POST["aadhar"]
            Suser.dob = request.POST["dob"]
            Suser.mobile_no = request.POST["mobile_no"]
            Suser.gender = request.POST["gender"]
            Suser.save()
            return redirect("loggedIn")
        else:
            return redirect("register")

def loggedIn(request):
    return render(request, 'loggedIn.html')

def login(request):
    return render(request, 'login.html')