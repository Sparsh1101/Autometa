from operator import mod
from re import L
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *
from .deploy import *


def is_rto(user):
    return user.groups.filter(name="rto").exists()


def is_police(user):
    return user.groups.filter(name="police").exists()


def is_customer(user):
    return user.groups.filter(name="customer").exists()


def index(request):
    return render(request, "index.html")


@login_required(login_url="registration:login")
@user_passes_test(is_rto, login_url="registration:login")
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
        return redirect("registration:rto_register")


@login_required(login_url="registration:login")
@user_passes_test(is_rto, login_url="registration:login")
def rto_register(request):
    isOwnerBool = request.session["isOwnerBool"]
    isVehicleBool = request.session["isVehicleBool"]
    aadhar = request.session["aadhar"]
    uniqueID = request.session["uniqueID"]
    vehicleInfoVars = ["uniqueID", "vehicleNo", "modelName", "vehicleColor"]
    ownerInfoVars = ["fName", "lName", "aadhar",
                     "dob", "gender", "email", "mobileNo"]

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
            vehicleInfo = getVehicleInfoFromUniqueID(
                register_contract, uniqueID)
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
                group = Group.objects.get(name="customer")
                group.user_set.add(Ruser)
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
                newOwnerInfoDict[ownerInfoVars[i]
                                 ] = request.POST[ownerInfoVars[i]]
            else:
                newOwnerInfoDict[ownerInfoVars[i]] = aadhar

        for i in range(len(vehicleInfoDict)):
            if vehicleInfoVars[i] != "uniqueID":
                newVehicleInfoDict[vehicleInfoVars[i]] = request.POST[
                    vehicleInfoVars[i]
                ]
            else:
                newVehicleInfoDict[vehicleInfoVars[i]] = uniqueID

        # Post req validation till gender

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

        if isVehicleBool == False or vehicleInfoDict == newVehicleInfoDict:
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

        return redirect("registration:rto_dashboard")


@login_required(login_url="registration:login")
@user_passes_test(is_rto, login_url="registration:login")
def rto_dashboard(request):
    return render(request, "rto-dashboard.html")


@login_required(login_url="registration:login")
@user_passes_test(is_rto, login_url="registration:login")
def vehicle_owners(request, id):
    owners = getOwnersFromUniqueID(register_contract, id)["data"]
    previousOwners = owners[:-1]
    currentOwner = owners[-1]
    prevLength = len(previousOwners)
    return render(
        request,
        "show-vehicle-owners.html",
        {
            "currentOwner": currentOwner,
            "previousOwners": previousOwners,
            "prevLength": prevLength,
            "uniqueID": id,
        },
    )


@login_required(login_url="registration:login")
@user_passes_test(is_rto, login_url="registration:login")
def owner_vehicles(request, id):
    vehicles = getVehiclesFromAadhar(register_contract, id)["data"]
    previouslyOwnedVehicles = []
    currentlyOwnedVehicles = []
    for vehicle in vehicles:
        if getOwnersFromUniqueID(register_contract, vehicle)["data"][-1] == id:
            currentlyOwnedVehicles.append(vehicle)
        else:
            previouslyOwnedVehicles.append(vehicle)
    prevLength = len(previouslyOwnedVehicles)
    currLength = len(currentlyOwnedVehicles)
    return render(
        request,
        "show-owner-vehicles.html",
        {
            "currentlyOwnedVehicles": currentlyOwnedVehicles,
            "previouslyOwnedVehicles": previouslyOwnedVehicles,
            "prevLength": prevLength,
            "currLength": currLength,
            "aadhar": id,
        },
    )


@login_required(login_url="registration:login")
@user_passes_test(is_rto, login_url="registration:login")
def owner(request, id=""):
    ownerInfoVars = ["fName", "lName", "aadhar",
                     "dob", "gender", "email", "mobileNo"]
    ownerInfoDict = {}
    if id == "":
        if request.method == "GET":
            return render(request, "get-aadhar-input-form.html")
        else:
            aadhar = request.POST["aadhar"]
            ownerInfo = getOwnerInfoFromAadhar(register_contract, aadhar)
            ownerInfo = ownerInfo["data"]
            if ownerInfo[0] == "":
                return redirect("registration:owner_noId")
            else:
                for i in range(len(ownerInfo)):
                    ownerInfoDict[ownerInfoVars[i]] = ownerInfo[i]
                return render(
                    request,
                    "show-owner-info.html",
                    {"ownerInfoDict": ownerInfoDict},
                )
    else:
        aadhar = id
        ownerInfo = getOwnerInfoFromAadhar(register_contract, aadhar)
        ownerInfo = ownerInfo["data"]
        if ownerInfo[0] == "":
            return redirect("registration:owner_noId")
        else:
            for i in range(len(ownerInfo)):
                ownerInfoDict[ownerInfoVars[i]] = ownerInfo[i]
            return render(
                request, "show-owner-info.html", {
                    "ownerInfoDict": ownerInfoDict}
            )


@login_required(login_url="registration:login")
@user_passes_test(is_rto, login_url="registration:login")
def vehicle(request, id=""):
    vehicleInfoVars = ["uniqueID", "vehicleNo", "modelName", "vehicleColor"]
    vehicleInfoDict = {}
    if id == "":
        if request.method == "GET":
            return render(request, "get-uniqueID-input-form.html")
        else:
            uniqueID = request.POST["uniqueID"]
            vehicleInfo = getVehicleInfoFromUniqueID(
                register_contract, uniqueID)
            vehicleInfo = vehicleInfo["data"]
            if vehicleInfo[1] == "":
                return redirect("registration:vehicle_noId")
            else:
                for i in range(len(vehicleInfo)):
                    vehicleInfoDict[vehicleInfoVars[i]] = vehicleInfo[i]
                return render(
                    request,
                    "show-vehicle-info.html",
                    {"vehicleInfoDict": vehicleInfoDict},
                )
    else:
        uniqueID = id
        vehicleInfo = getVehicleInfoFromUniqueID(register_contract, uniqueID)
        vehicleInfo = vehicleInfo["data"]
        if vehicleInfo[1] == "":
            return redirect("registration:vehicle_noId")
        else:
            for i in range(len(vehicleInfo)):
                vehicleInfoDict[vehicleInfoVars[i]] = vehicleInfo[i]
            return render(
                request,
                "show-vehicle-info.html",
                {"vehicleInfoDict": vehicleInfoDict},
            )


@login_required(login_url="registration:login")
@user_passes_test(is_rto, login_url="registration:login")
def rto_choose_update(request):
    return render(request, "rto-choose-update.html")


@login_required(login_url="registration:login")
@user_passes_test(is_rto, login_url="registration:login")
def rto_update_vehicle_info_1(request):
    if request.method == "GET":
        return render(request, "get-uniqueID-input-form.html")
    else:
        uniqueID = request.POST["uniqueID"]
        vehicleInfo = getVehicleInfoFromUniqueID(register_contract, uniqueID)
        vehicleInfo = vehicleInfo["data"]
        vehicleInfoVars = ["uniqueID", "vehicleNo",
                           "modelName", "vehicleColor"]
        vehicleInfoDict = {}
        for i in range(len(vehicleInfo)):
            vehicleInfoDict[vehicleInfoVars[i]] = vehicleInfo[i]
        if vehicleInfo[1] == "":
            print("Vehicle doesn't exist")
            return render(request, "get-uniqueID-input-form.html")
        else:
            request.session["vehicleInfoDict"] = vehicleInfoDict
            return redirect("registration:rto_update_vehicle_info_2")


@login_required(login_url="registration:login")
@user_passes_test(is_rto, login_url="registration:login")
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
        vehicleInfoVars = ["uniqueID", "vehicleNo",
                           "modelName", "vehicleColor"]
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
        return redirect("registration:rto_dashboard")


@login_required(login_url="registration:login")
@user_passes_test(is_rto, login_url="registration:login")
def rto_update_owner_info_1(request):
    if request.method == "GET":
        return render(request, "get-aadhar-input-form.html")
    else:
        aadhar = request.POST["aadhar"]
        ownerInfo = getOwnerInfoFromAadhar(register_contract, aadhar)
        ownerInfo = ownerInfo["data"]
        # vehicleInfoVars = ["uniqueID", "vehicleNo", "modelName", "vehicleColor"]
        # vehicleInfoDict = {}
        ownerInfoVars = [
            "fName",
            "lName",
            "aadhar",
            "dob",
            "gender",
            "email",
            "mobileNo",
        ]
        ownerInfoDict = {}
        for i in range(len(ownerInfo)):
            ownerInfoDict[ownerInfoVars[i]] = ownerInfo[i]
        if ownerInfo[0] == "":
            print("User doesn't exist")
            return render(request, "get-aadhar-input-form.html")
        else:
            request.session["ownerInfoDict"] = ownerInfoDict
            return redirect("registration:rto_update_owner_info_2")


@login_required(login_url="registration:login")
@user_passes_test(is_rto, login_url="registration:login")
def rto_update_owner_info_2(request):
    ownerInfoDict = request.session["ownerInfoDict"]
    if request.method == "GET":
        return render(
            request, "rto-update-owner-info-form.html", {
                "ownerInfoDict": ownerInfoDict}
        )
    else:
        aadhar = ownerInfoDict["aadhar"]
        ownerInfoVars = [
            "fName",
            "lName",
            "aadhar",
            "dob",
            "gender",
            "email",
            "mobileNo",
        ]
        newOwnerInfoDict = {}
        for i in range(len(ownerInfoDict)):
            if ownerInfoVars[i] != "aadhar":
                newOwnerInfoDict[ownerInfoVars[i]
                                 ] = request.POST[ownerInfoVars[i]]
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
        return redirect("registration:rto_dashboard")


def login(request, id):
    form = LoginForm()
    message = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                auth_login(request, user)
                if is_rto(user) and id == "rto":
                    return redirect("registration:rto_dashboard")
                elif is_police(user) and id == "police":
                    return HttpResponse("<h1>Police Dashboard</h1>")
                elif is_customer(user) and id == "customer":
                    return HttpResponse("<h1>Customer Dashboard</h1>")
                else:
                    message = "Access Denied!"
                    return render(
                        request,
                        "login.html",
                        context={
                            "form": form,
                            "message": message,
                            "id": id,
                        },
                    )
            else:
                message = "Username or Password is incorrect!"
                return render(
                    request,
                    "login.html",
                    context={
                        "form": form,
                        "message": message,
                        "id": id,
                    },
                )
        else:
            return redirect("registration:login")
    return render(
        request,
        "login.html",
        context={
            "form": form,
            "message": message,
            "id": id,
        },
    )


@login_required(login_url="registration:index")
def logoutU(request):
    logout(request)
    return redirect("registration:index")
