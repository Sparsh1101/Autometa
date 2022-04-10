from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *
from .deploy import *
from .helper_functions import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def check_register(request):
    if request.method == "GET":
        return render(request, "check-register.html")
    else:
        uniqueID = request.POST["uniqueID"]
        aadhar = request.POST["aadhar"]
        isOwnerBool = isOwner(register_contract, aadhar)
        isOwnerBool = isOwnerBool["data"]
        isVehicleBool = isVehicle(register_contract, uniqueID)
        isVehicleBool = isVehicleBool["data"]
        request.session["isOwnerBool"] = isOwnerBool
        request.session["isVehicleBool"] = isVehicleBool
        request.session["aadhar"] = aadhar
        request.session["uniqueID"] = uniqueID
        return redirect('/rto/register')

def register(request):
    isOwnerBool = request.session["isOwnerBool"]
    isVehicleBool = request.session["isVehicleBool"]
    aadhar = request.session["aadhar"]
    uniqueID = request.session["uniqueID"]
    if request.method == "GET":        
        if isOwnerBool:
            ownerInfo = getOwnerInfoFromAdhaar(register_contract, aadhar)
            ownerInfo = ownerInfo["data"]
            fName = ownerInfo[0]
            lName = ownerInfo[1]
            dob = ownerInfo[3]
            gender = ownerInfo[4]
            email = ownerInfo[5]
            mobileNo = ownerInfo[6]
            user_creation_form = ""
        else:
            user_creation_form = UserCreationForm()
            fName = ""
            lName = ""
            dob = ""
            gender = ""
            email = ""
            mobileNo = ""

        if isVehicleBool:
            vehicleInfo = getVehicleInfoFromUniqueID(register_contract, uniqueID)
            vehicleInfo = vehicleInfo["data"]
            vehicleNo = vehicleInfo[1]
            modelName = vehicleInfo[2]
            vehicleColor = vehicleInfo[3]
        else:
            vehicleNo = ""
            modelName = ""
            vehicleColor = ""

        return render(request, "register.html", {
            "user_creation_form": user_creation_form,
            "aadhar": aadhar,
            "uniqueID": uniqueID, 
            "fName": fName,
            "lName": lName,
            "dob": dob,
            "gender": gender,
            "email": email, 
            "mobileNo": mobileNo,
            "vehicleNo": vehicleNo,
            "modelName": modelName,
            "vehicleColor": vehicleColor,
            "isOwnerBool": isOwnerBool,
        })
    else:
        if isOwnerBool == False:
            user_creation_form = UserCreationForm(request.POST)
            if user_creation_form.is_valid():
                Ruser = user_creation_form.save(commit=False)
                Ruser.save()
            else:
                return render(request, "register.html")
        vehicleNo = request.POST["vehicleNo"]
        modelName = request.POST["modelName"]
        vehicleColor = request.POST["vehicleColor"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        email = request.POST["email"]
        mobile_no = request.POST["mobile_no"]
        storeInfo(register_contract, uniqueID, vehicleNo, modelName, vehicleColor, fname, lname, aadhar, dob, gender, email, mobile_no)
        print("Store Successful")
        return redirect('/rto')

def loggedIn(request):
    return render(request, 'loggedIn.html')

def login(request):
    return render(request, 'login.html')

def rto_dashboard(request):
    return render(request, "rto_dashboard.html")

def rto_owner(request):
    if request.method == "GET":
        return render(request, "rto_owner_form.html")
    else:
        aadhar = request.POST["aadhar"]
        ownerInfo = getOwnerInfoFromAdhaar(register_contract, aadhar)
        ownerInfo = ownerInfo["data"]
        vehicleIDs = getVehiclesFromAdhaar(register_contract, aadhar)
        vehicleIDs = vehicleIDs["data"]
        print(vehicleIDs)
        return render(request, "rto_owner.html", {"owner": ownerInfo})
    
def rtologin(request):
    # if request.method == "GET":
    #     form = CustomAuthenticationForm()
    #     return render(request, "registration/login.html", {"form": form})
    # else:
        # form = CustomAuthenticationForm(request.POST)
        # username = request.POST["username"]
        # password = request.POST["password"]
        # grp = request.POST["groups"]
        # if User.objects.filter(username=username).exists():
        #     user = User.objects.get(username=username)
        #     if user.check_password(password):
        #         our_user = custom_user_filter(user)
        #         if our_user == None:
        #             return render(
        #                 request,
        #                 "registration/login.html",
        #                 {"form": form, "my_messages": {"error": "Access Denied."}},
                    # )
    return render(request, 'login-rto.html')

def customerlogin(request):
    return render(request, 'login-customer.html')
