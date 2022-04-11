from operator import mod
from re import L
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
    return render(request, "index.html")


def rto_check_register(request):
    if request.method == "GET":
        return render(request, "rto-check-register.html")
    else:
        uniqueID = request.POST["uniqueID"]
        aadhar = request.POST["aadhar"]
        isOwnerBool = isOwner(register_contract, aadhar)
        isOwnerBool = isOwnerBool["data"]
        isVehicleBool = isVehicle(register_contract, uniqueID)
        isVehicleBool = isVehicleBool["data"]
        if isOwnerBool:
            ownerInfo = getOwnerInfoFromAadhar(register_contract, aadhar)
            ownerInfo = ownerInfo["data"]
            vehicleIDs = getVehiclesFromAadhar(register_contract, aadhar)
            vehicleIDs = vehicleIDs["data"]
            if vehicleIDs[-1] == uniqueID:
                return render(request, "rto-check-register.html")
        
        request.session["isOwnerBool"] = isOwnerBool
        request.session["isVehicleBool"] = isVehicleBool
        request.session["aadhar"] = aadhar
        request.session["uniqueID"] = uniqueID
        return redirect("/rto/register")


def rto_register(request):
    isOwnerBool = request.session["isOwnerBool"]
    isVehicleBool = request.session["isVehicleBool"]
    aadhar = request.session["aadhar"]
    uniqueID = request.session["uniqueID"]
    vehicleInfoVars = ["uniqueID", "vehicleNo", "modelName", "vehicleColor"]
    ownerInfoVars = ["fName", "lName", "aadhar", "dob", "gender", "email", "mobileNo"]

    if request.method == "GET":
        ownerInfoDict = {}
        vehicleInfoDict = {}

        if isOwnerBool:
            ownerInfo = getOwnerInfoFromAadhar(register_contract, aadhar)
            ownerInfo = ownerInfo["data"]
            user_creation_form = ""
        else:
            ownerInfo = ["", "", aadhar, "", "", "", ""]
            user_creation_form = UserCreationForm()

        for i in range(len(ownerInfo)):
            ownerInfoDict[ownerInfoVars[i]] = ownerInfo[i]

        if isVehicleBool:
            vehicleInfo = getVehicleInfoFromUniqueID(register_contract, uniqueID)
            vehicleInfo = vehicleInfo["data"]
        else:
            vehicleInfo = [uniqueID, "", "", ""]

        for i in range(len(vehicleInfo)):
            vehicleInfoDict[vehicleInfoVars[i]] = vehicleInfo[i]

        request.session["ownerInfoDict"] = ownerInfoDict
        request.session["vehicleInfoDict"] = vehicleInfoDict

        return render(
            request,
            "rto-register.html",
            {
                "user_creation_form": user_creation_form,
                "aadhar": aadhar,
                "uniqueID": uniqueID,
                "ownerInfoDict": ownerInfoDict,
                "vehicleInfoDict": vehicleInfoDict,
            },
        )
    else:
        ownerInfoDict = request.session["ownerInfoDict"]
        vehicleInfoDict = request.session["vehicleInfoDict"]
        newOwnerInfoDict = {}
        newVehicleInfoDict = {}
        if isOwnerBool == False:
            user_creation_form = UserCreationForm(request.POST)
            if user_creation_form.is_valid():
                Ruser = user_creation_form.save(commit=False)
                Ruser.save()
            else:
                return render(
                    request,
                    "rto-register.html",
                    {
                        "user_creation_form": user_creation_form,
                        "aadhar": aadhar,
                        "uniqueID": uniqueID,
                        "ownerInfoDict": ownerInfoDict,
                        "vehicleInfoDict": vehicleInfoDict,
                    },
                )

        for i in range(len(ownerInfoDict)):
            if ownerInfoVars[i] != "aadhar":
                newOwnerInfoDict[ownerInfoVars[i]] = request.POST[ownerInfoVars[i]]
            else:
                newOwnerInfoDict[ownerInfoVars[i]] = aadhar

        for i in range(len(vehicleInfoDict)):
            if vehicleInfoVars[i] != "uniqueID":
                newVehicleInfoDict[vehicleInfoVars[i]] = request.POST[
                    vehicleInfoVars[i]
                ]
            else:
                newVehicleInfoDict[vehicleInfoVars[i]] = uniqueID

        storeInfo(
            register_contract,
            uniqueID,
            newVehicleInfoDict["vehicleNo"],
            newVehicleInfoDict["modelName"],
            newVehicleInfoDict["vehicleColor"],
            newOwnerInfoDict["fName"],
            newOwnerInfoDict["lName"],
            aadhar,
            newOwnerInfoDict["dob"],
            newOwnerInfoDict["gender"],
            newOwnerInfoDict["email"],
            newOwnerInfoDict["mobileNo"],
        )

        if  isVehicleBool == False or vehicleInfoDict == newVehicleInfoDict:
            pass
        else:
            updateVehicleInfo(
                register_contract,
                uniqueID,
                newVehicleInfoDict["vehicleNo"],
                newVehicleInfoDict["modelName"],
                newVehicleInfoDict["vehicleColor"],
            )
            print("Updated Vehicle Info")

        if isOwnerBool == False or ownerInfoDict == newOwnerInfoDict:
            pass
        else:
            updateOwnerInfo(
                register_contract,
                newOwnerInfoDict["fName"],
                newOwnerInfoDict["lName"],
                aadhar,
                newOwnerInfoDict["dob"],
                newOwnerInfoDict["gender"],
                newOwnerInfoDict["email"],
                newOwnerInfoDict["mobileNo"],
            )
            print("Updated Owner Info")
        
        del request.session["isOwnerBool"]
        del request.session["isVehicleBool"]
        del request.session["aadhar"]
        del request.session["uniqueID"]
        del request.session["ownerInfoDict"]
        del request.session["vehicleInfoDict"]

        return redirect("/rto")


def loggedIn(request):
    return render(request, "loggedIn.html")


def login(request):
    return render(request, "login.html")


def rto_dashboard(request):
    return render(request, "rto-dashboard.html")


def rto_owner(request):
    if request.method == "GET":
        return render(request, "rto-get-aadhar-input-form.html")
    else:
        aadhar = request.POST["aadhar"]
        ownerInfo = getOwnerInfoFromAadhar(register_contract, aadhar)
        ownerInfo = ownerInfo["data"]
        vehicleIDs = getVehiclesFromAadhar(register_contract, aadhar)
        vehicleIDs = vehicleIDs["data"]
        print(vehicleIDs)
        return render(request, "rto-show-owner-info.html", {"owner": ownerInfo})

def rto_vehicle(request):
    if request.method == "GET":
        return render(request, "rto-get-uniqueID-input-form.html")
    else:
        uniqueID = request.POST["uniqueID"]
        vehicleInfo = getVehicleInfoFromUniqueID(register_contract, uniqueID)
        vehicleInfo = vehicleInfo["data"]
        ownerAadhars = getOwnersFromUniqueID(register_contract, uniqueID)
        ownerAadhars = ownerAadhars["data"]
        print(ownerAadhars)
        return render(request, "rto-show-vehicle-info.html", {"vehicle": vehicleInfo})

def rto_choose_update(request):
        return render(request, "rto-choose-update.html")

def rto_update_vehicle_info_1(request):
    if request.method == "GET":
        return render(request, "rto-get-uniqueID-input-form.html")
    else:
        uniqueID = request.POST["uniqueID"]
        vehicleInfo = getVehicleInfoFromUniqueID(register_contract, uniqueID)
        vehicleInfo = vehicleInfo["data"]
        vehicleInfoVars = ["uniqueID", "vehicleNo", "modelName", "vehicleColor"]
        vehicleInfoDict = {}
        for i in range(len(vehicleInfo)):
            vehicleInfoDict[vehicleInfoVars[i]] = vehicleInfo[i]
        if (vehicleInfo[1] == ''):
            print("Vehicle doesn't exist")
            return render(request, "rto-get-uniqueID-input-form.html")
        else:
            request.session["vehicleInfoDict"] = vehicleInfoDict
            return redirect('/rto/update-vehicle-info-2')

def rto_update_vehicle_info_2(request):
    vehicleInfoDict = request.session["vehicleInfoDict"]
    if request.method == "GET":
        return render(
            request,
            "rto-update-vehicle-info-form.html",
            {"vehicleInfoDict": vehicleInfoDict},
        )
    else:
        uniqueID = vehicleInfoDict["uniqueID"]
        vehicleInfoVars = ["uniqueID", "vehicleNo", "modelName", "vehicleColor"]
        newVehicleInfoDict = {}
        for i in range(len(vehicleInfoDict)):
            if vehicleInfoVars[i] != "uniqueID":
                newVehicleInfoDict[vehicleInfoVars[i]] = request.POST[
                    vehicleInfoVars[i]
                ]
            else:
                newVehicleInfoDict[vehicleInfoVars[i]] = uniqueID
        updateVehicleInfo(
            register_contract,
            uniqueID,
            newVehicleInfoDict["vehicleNo"],
            newVehicleInfoDict["modelName"],
            newVehicleInfoDict["vehicleColor"],
        )
        del request.session["vehicleInfoDict"]
        print("Updated Vehicle Info")
        return redirect("/rto")

def rto_update_owner_info_1(request):
    if request.method == "GET":
        return render(request, "rto-get-aadhar-input-form.html")
    else:
        aadhar = request.POST["aadhar"]
        ownerInfo = getOwnerInfoFromAadhar(register_contract, aadhar)
        ownerInfo = ownerInfo["data"]
        # vehicleInfoVars = ["uniqueID", "vehicleNo", "modelName", "vehicleColor"]
        # vehicleInfoDict = {}
        ownerInfoVars = ["fName", "lName", "aadhar", "dob", "gender", "email", "mobileNo"]
        ownerInfoDict = {}
        for i in range(len(ownerInfo)):
            ownerInfoDict[ownerInfoVars[i]] = ownerInfo[i]
        if (ownerInfo[0] == ''):
            print("User doesn't exist")
            return render(request, "rto-get-aadhar-input-form.html")
        else:
            request.session["ownerInfoDict"] = ownerInfoDict
            return redirect('/rto/update-owner-info-2')

def rto_update_owner_info_2(request):
    ownerInfoDict = request.session["ownerInfoDict"]
    if request.method == "GET":
        return render(request, "rto-update-owner-info-form.html", {"ownerInfoDict": ownerInfoDict})
    else:
        aadhar = ownerInfoDict['aadhar']
        ownerInfoVars = ["fName", "lName", "aadhar", "dob", "gender", "email", "mobileNo"]
        newOwnerInfoDict = {}
        for i in range(len(ownerInfoDict)):
            if ownerInfoVars[i] != "aadhar":
                newOwnerInfoDict[ownerInfoVars[i]] = request.POST[ownerInfoVars[i]]
            else:
                newOwnerInfoDict[ownerInfoVars[i]] = aadhar
        updateOwnerInfo(
            register_contract,
            newOwnerInfoDict["fName"],
            newOwnerInfoDict["lName"],
            aadhar,
            newOwnerInfoDict["dob"],
            newOwnerInfoDict["gender"],
            newOwnerInfoDict["email"],
            newOwnerInfoDict["mobileNo"],
        )
        del request.session["ownerInfoDict"]
        print("Updated Owner Info")
        return redirect('/rto')


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
    return render(request, "login-rto.html")


def customerlogin(request):
    return render(request, "login-customer.html")
