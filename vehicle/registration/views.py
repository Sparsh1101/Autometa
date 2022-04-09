from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *
from .deploy import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "GET":
        form = UserInfoForm()
        user_creation_form = UserCreationForm()
        vehicle_form = VehicleInfoForm()
        return render(
            request,
            "register.html",
            {
                "form": form,
                "user_creation_form": user_creation_form,
                "vehicle_form": vehicle_form,
            },
        )
    if request.method == "POST":
        form = UserInfoForm(request.POST)
        user_creation_form = UserCreationForm(request.POST)
        vehicle_form = VehicleInfoForm(request.POST)
        if form.is_valid() and user_creation_form.is_valid():
            Ruser = user_creation_form.save(commit=False)
            Ruser.save()
            uniqueID = request.POST["uniqueID"]
            vehicleNo = request.POST["vehicleNo"]
            modelName = request.POST["modelName"]
            vehicleColor = request.POST["vehicleColor"]
            fname = request.POST["fname"]
            lname = request.POST["lname"]
            aadhar = request.POST["aadhar"]
            dob = '10/11/1993'
            gender = request.POST["gender"]
            email = request.POST["email"]
            mobile_no = request.POST["mobile_no"]
            storeInfo(register_contract, uniqueID, vehicleNo, modelName, vehicleColor, fname, lname, aadhar, dob, gender, email, mobile_no)
            return redirect('/rto')
            
    else:
        form = UserInfoForm()
        user_creation_form = UserCreationForm()
        vehicle_form = VehicleInfoForm()
    
    return render(request, 'register.html', {'form': form, "user_creation_form": user_creation_form, "vehicle_form": vehicle_form,})

def loggedIn(request):
    return render(request, 'loggedIn.html')

def login(request):
    return render(request, 'login.html')

def rto_dashboard(request):
    return render(request, "rto_dashboard.html")

def rto_owner(request):
    if request.method == "GET":
        return render(request, "rto_owner_form.html")
    if request.method == "POST":
        aadhar = request.POST["aadhar"]
        ownerInfo = getOwnerInfoFromAdhaar(register_contract, aadhar)
        ownerInfo = ownerInfo["data"]
        return render(request, "rto_owner.html", {"owner": ownerInfo})
            
    else:
        form = UserInfoForm()
        user_creation_form = UserCreationForm()
        vehicle_form = VehicleInfoForm()
    
    return render(request, 'register.html', {'form': form, "user_creation_form": user_creation_form, "vehicle_form": vehicle_form,})