from dis import dis
from operator import mod
from re import L
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import *
from .forms import *
from .deploy import *
import qrcode
import qrcode.image.svg
import os
from io import BytesIO
from django.conf import settings
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from django.http.response import HttpResponse
from PIL import Image


def download_file(request, id):
    url1 = request.build_absolute_uri()
    url2 = url1.split("download_file")
    url = url2[0] + "vehicle-qr" + url2[1]
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(url, image_factory=factory, box_size=20)
    stream = BytesIO()
    img.save(stream)
    svg = stream.getvalue().decode()
    img.save(settings.MEDIA_ROOT + "/" + url2[1] + ".svg")
    drawing = svg2rlg(settings.MEDIA_ROOT + "/" + url2[1] + ".svg")
    renderPM.drawToFile(drawing, settings.MEDIA_ROOT +
                        "/" + url2[1] + ".png", fmt="PNG")
    filename = url2[1]
    filepath = settings.MEDIA_ROOT + "/" + filename + ".png"
    im = Image.open(filepath)
    response = HttpResponse(content_type="image/png")
    response["Content-Disposition"] = "attachment; filename=%s.png" % filename
    im.save(response, "png")
    os.remove(settings.MEDIA_ROOT + "/" + url2[1] + ".svg")
    os.remove(settings.MEDIA_ROOT + "/" + url2[1] + ".png")
    return response


def index(request):
    return render(request, "index.html")


@login_required(login_url="registration:login")
@user_passes_test(is_rto, login_url="registration:login")
def rto_check_register(request):
    if request.method == "GET":
        form = CheckRegisterForm()
        return render(request, "rto-check-register.html", {"form": form})
    else:
        form = CheckRegisterForm(request.POST)
        if form.is_valid():
            uniqueID = request.POST["uniqueID"]
            aadhar = request.POST["aadhar"]
            isOwnerBool = isOwner(register_contract, aadhar)["data"]
            isVehicleBool = isVehicle(register_contract, uniqueID)["data"]
            if isOwnerBool:
                ownerInfo = getOwnerInfoFromAadhar(register_contract, aadhar)
                ownerInfo = ownerInfo["data"]
                vehicleIDs = getVehiclesFromAadhar(register_contract, aadhar)
                vehicleIDs = vehicleIDs["data"]
                if vehicleIDs[-1] == uniqueID:
                    message = "User already owns this vehicle!"
                    return render(
                        request,
                        "rto-check-register.html",
                        {"form": form, "message": message},
                    )

            request.session["isOwnerBool"] = isOwnerBool
            request.session["isVehicleBool"] = isVehicleBool
            request.session["aadhar"] = aadhar
            request.session["uniqueID"] = uniqueID
            return redirect("registration:rto_register")

        else:
            return render(request, "rto-check-register.html", {"form": form})


@login_required(login_url="registration:login")
@user_passes_test(is_rto, login_url="registration:login")
def rto_register(request):
    isOwnerBool = request.session["isOwnerBool"]
    isVehicleBool = request.session["isVehicleBool"]
    aadhar = request.session["aadhar"]
    uniqueID = request.session["uniqueID"]
    vehicleInfoVars = ["exists2", "uniqueID",
                       "vehicleNo", "modelName", "vehicleColor"]
    ownerInfoVars = [
        "exists1",
        "fName",
        "lName",
        "aadhar",
        "dob",
        "userID",
        "email",
        "mobileNo",
        "gender",
    ]

    if request.method == "GET":
        ownerInfoDict = {}
        vehicleInfoDict = {}

        if isOwnerBool:
            ownerInfo = getOwnerInfoFromAadhar(register_contract, aadhar)
            ownerInfo = ownerInfo["data"]
        else:
            ownerInfo = ["", "", "", aadhar, "", "", "", ("", "", "")]

        for i in range(len(ownerInfo) - 2):
            ownerInfoDict[ownerInfoVars[i]] = ownerInfo[i]

        (
            ownerInfoDict["mobileNo"],
            ownerInfoDict["email"],
            ownerInfoDict["gender"],
        ) = ownerInfo[-1]

        if isVehicleBool:
            vehicleInfo = getVehicleInfoFromUniqueID(
                register_contract, uniqueID)
            vehicleInfo = vehicleInfo["data"]
        else:
            vehicleInfo = ["", uniqueID, "", "", "", "", ("", "", "", "")]

        for i in range(len(vehicleInfo) - 2):
            vehicleInfoDict[vehicleInfoVars[i]] = vehicleInfo[i]

        request.session["ownerInfoDict"] = ownerInfoDict
        request.session["vehicleInfoDict"] = vehicleInfoDict

        initial_dict = {**ownerInfoDict, **vehicleInfoDict}
        form = RegisterForm(request.POST or None, initial=initial_dict)
        return render(
            request,
            "rto-register.html",
            {
                "form": form,
                "aadhar": aadhar,
                "uniqueID": uniqueID,
            },
        )
    else:
        ownerInfoDict = request.session["ownerInfoDict"]
        vehicleInfoDict = request.session["vehicleInfoDict"]
        newOwnerInfoDict = {}
        newVehicleInfoDict = {}
        if isOwnerBool == False:
            form = RegisterForm(request.POST or None)
            if form.is_valid():
                Ruser = User.objects.create_user(username=aadhar, password=aadhar)
                our_user = Customer(user=Ruser, first_password=aadhar, password_changed=False)
                our_user.save()
                Ruser.save()
                group = Group.objects.get(name="customer")
                group.user_set.add(Ruser)
            else:
                return render(
                    request,
                    "rto-register.html",
                    {
                        "form": form,
                        "aadhar": aadhar,
                        "uniqueID": uniqueID,
                    },
                )
        else:
            Ruser = User.objects.get(username=aadhar)

        for i in range(1, len(ownerInfoDict)):
            if ownerInfoVars[i] == "aadhar":
                newOwnerInfoDict[ownerInfoVars[i]] = aadhar
            elif ownerInfoVars[i] == "exists1":
                newOwnerInfoDict["exists1"] = ownerInfoDict["exists1"]
            elif ownerInfoVars[i] == "userID":
                newOwnerInfoDict[ownerInfoVars[i]] = Ruser.id
            else:
                newOwnerInfoDict[ownerInfoVars[i]
                                 ] = request.POST[ownerInfoVars[i]]

        for i in range(1, len(vehicleInfoDict)):
            if vehicleInfoVars[i] != "uniqueID":
                newVehicleInfoDict[vehicleInfoVars[i]] = request.POST[
                    vehicleInfoVars[i]
                ]
            else:
                newVehicleInfoDict[vehicleInfoVars[i]] = uniqueID
            newVehicleInfoDict["exists2"] = vehicleInfoDict["exists2"]

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
            str(Ruser.id),
            (
                newOwnerInfoDict["mobileNo"],
                newOwnerInfoDict["email"],
                newOwnerInfoDict["gender"],
            ),
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

        message = "New Record created successfully!"

        return render(
            request,
            "rto-dashboard.html",
            {"message": message},
        )


@login_required(login_url="registration:login")
@user_passes_test(is_rto, login_url="registration:login")
def rto_dashboard(request):
    return render(request, "rto-dashboard.html")


@login_required(login_url="registration:login")
@user_passes_test(is_police, login_url="registration:login")
def police_dashboard(request):
    return render(request, "police-dashboard.html")


@login_required(login_url="registration:login")
@user_passes_test(is_customer, login_url="registration:login")
@password_change_required
def customer_dashboard(request):
    return render(request, "customer-dashboard.html")


@login_required(login_url="registration:login")
@user_passes_test(is_authorised_user, login_url="registration:login")
def vehicle_owners(request, id):
    owners = getOwnersFromUniqueID(register_contract, id)["data"]
    previousOwners = owners[:-1]
    currentOwner = owners[-1]
    prevLength = len(previousOwners)
    isPolice = is_police(request.user)
    return render(
        request,
        "show-vehicle-owners.html",
        {
            "currentOwner": currentOwner,
            "previousOwners": previousOwners,
            "prevLength": prevLength,
            "uniqueID": id,
            "isPolice": isPolice,
        },
    )


@login_required(login_url="registration:login")
def owner_vehicles(request, id):
    isCustomer = is_customer(request.user)
    isPolice = is_police(request.user)
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
            "isCustomer": isCustomer,
            "isPolice": isPolice,
        },
    )


@login_required(login_url="registration:login")
def owner(request, id=""):
    ownerInfoVars = [
        "exists1",
        "fName",
        "lName",
        "aadhar",
        "dob",
        "userID",
        "email",
        "mobileNo",
        "gender",
    ]
    ownerInfoDict = {}
    isCustomer = is_customer(request.user)
    isPolice = is_police(request.user)

    if id == "":
        if request.method == "GET":
            form = AadharInputForm()
            return render(request, "get-aadhar-input-form.html", {"form": form})
        else:
            form = AadharInputForm(request.POST)
            if form.is_valid():
                aadhar = request.POST["aadhar"]
                ownerInfo = getOwnerInfoFromAadhar(
                    register_contract, aadhar)["data"]
                for i in range(len(ownerInfo) - 2):
                    ownerInfoDict[ownerInfoVars[i]] = ownerInfo[i]
                    (
                        ownerInfoDict["mobileNo"],
                        ownerInfoDict["email"],
                        ownerInfoDict["gender"],
                    ) = ownerInfo[-1]
                return render(
                    request,
                    "show-owner-info.html",
                    {
                        "ownerInfoDict": ownerInfoDict,
                        "isCustomer": isCustomer,
                        "isPolice": isPolice,
                    },
                )
            else:
                return render(request, "get-aadhar-input-form.html", {"form": form})
    else:
        aadhar = id
        ownerInfo = getOwnerInfoFromAadhar(register_contract, aadhar)
        ownerInfo = ownerInfo["data"]
        if ownerInfo[0] == "":
            return redirect("registration:owner_noId")
        else:
            for i in range(len(ownerInfo) - 2):
                ownerInfoDict[ownerInfoVars[i]] = ownerInfo[i]
            (
                ownerInfoDict["mobileNo"],
                ownerInfoDict["email"],
                ownerInfoDict["gender"],
            ) = ownerInfo[-1]
            return render(
                request,
                "show-owner-info.html",
                {
                    "ownerInfoDict": ownerInfoDict,
                    "isCustomer": isCustomer,
                    "isPolice": isPolice,
                },
            )


@login_required(login_url="registration:login")
@user_passes_test(is_customer, login_url="registration:login")
def customer_profile(request):
    user_id = request.user.id
    aadhar = getAadharfromUserId(register_contract, str(user_id))["data"]
    print("aadhar:", aadhar)
    return redirect("registration:owner", aadhar)


@login_required(login_url="registration:login")
@user_passes_test(is_customer, login_url="registration:login")
def customer_qr(request):
    user_id = request.user.id
    aadhar = getAadharfromUserId(register_contract, str(user_id))
    aadhar = aadhar["data"]
    isCustomer = is_customer(request.user)
    vehicles = getVehiclesFromAadhar(register_contract, aadhar)["data"]
    currentlyOwnedVehicles = []
    for vehicle in vehicles:
        if getOwnersFromUniqueID(register_contract, vehicle)["data"][-1] == aadhar:
            currentlyOwnedVehicles.append(vehicle)
    currLength = len(currentlyOwnedVehicles)
    return render(
        request,
        "customer-qr.html",
        {
            "currentlyOwnedVehicles": currentlyOwnedVehicles,
            "currLength": currLength,
            "aadhar": aadhar,
            "isCustomer": isCustomer,
        },
    )


def vehicle_qr(request, id):
    if request.user.is_authenticated:
        auth = True
    else:
        auth = False
    vehicleInfoVars = ["exists2", "uniqueID",
                       "vehicleNo", "modelName", "vehicleColor"]
    vehicleInfoDict = {}
    uniqueID = id
    vehicleInfo = getVehicleInfoFromUniqueID(register_contract, uniqueID)
    vehicleInfo = vehicleInfo["data"]
    for i in range(len(vehicleInfo) - 2):
        vehicleInfoDict[vehicleInfoVars[i]] = vehicleInfo[i]
    FIRs = vehicleInfo[-1]
    owners = getOwnersFromUniqueID(register_contract, uniqueID)["data"]
    prevOwnersNum = len(owners) - 1
    url = request.build_absolute_uri()
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(url, image_factory=factory, box_size=20)
    stream = BytesIO()
    img.save(stream)
    svg = stream.getvalue().decode()
    return render(
        request,
        "vehicle-qr.html",
        {
            "vehicleInfoDict": vehicleInfoDict,
            "FIRs": FIRs,
            "svg": svg,
            "auth": auth,
            "prevOwnersNum": prevOwnersNum,
        },
    )


@login_required(login_url="registration:login")
def vehicle(request, id=""):
    vehicleInfoVars = ["exists2", "uniqueID",
                       "vehicleNo", "modelName", "vehicleColor"]
    vehicleInfoDict = {}
    isCustomer = is_customer(request.user)
    isPolice = is_police(request.user)
    form = UniqueIDInputForm()
    if id == "":
        if request.method == "GET":
            return render(request, "get-uniqueID-input-form.html", {"form": form})
        else:
            form = UniqueIDInputForm(request.POST)
            if form.is_valid():
                uniqueID = request.POST["uniqueID"]
                vehicleInfo = getVehicleInfoFromUniqueID(register_contract, uniqueID)[
                    "data"
                ]
                for i in range(len(vehicleInfo) - 2):
                    vehicleInfoDict[vehicleInfoVars[i]] = vehicleInfo[i]
                FIRs = vehicleInfo[-1]
                owners = getOwnersFromUniqueID(
                    register_contract, uniqueID)["data"]
                prevOwnersNum = len(owners) - 1
                return render(
                    request,
                    "show-vehicle-info.html",
                    {
                        "vehicleInfoDict": vehicleInfoDict,
                        "FIRs": FIRs,
                        "isCustomer": isCustomer,
                        "isPolice": isPolice,
                        "prevOwnersNum": prevOwnersNum,
                    },
                )
            else:
                return render(request, "get-uniqueID-input-form.html", {"form": form})
    else:
        uniqueID = id
        vehicleInfo = getVehicleInfoFromUniqueID(register_contract, uniqueID)
        vehicleInfo = vehicleInfo["data"]
        if vehicleInfo[1] == "":
            return redirect("registration:vehicle_noId")
        else:
            for i in range(len(vehicleInfo) - 2):
                vehicleInfoDict[vehicleInfoVars[i]] = vehicleInfo[i]
            FIRs = vehicleInfo[-1]
            owners = getOwnersFromUniqueID(register_contract, uniqueID)["data"]
            prevOwnersNum = len(owners) - 1
            return render(
                request,
                "show-vehicle-info.html",
                {
                    "vehicleInfoDict": vehicleInfoDict,
                    "FIRs": FIRs,
                    "isCustomer": isCustomer,
                    "isPolice": isPolice,
                    "prevOwnersNum": prevOwnersNum,
                },
            )


@login_required(login_url="registration:login")
@user_passes_test(is_police, login_url="registration:login")
def police_vehicle(request, id=""):
    vehicleInfoVars = ["exists2", "uniqueID",
                       "vehicleNo", "modelName", "vehicleColor"]
    vehicleInfoDict = {}
    if id == "":
        if request.method == "GET":
            form = UniqueIDInputForm()
            return render(request, "get-uniqueID-input-form.html", {"form": form})
        else:
            form = UniqueIDInputForm(request.POST)
            if form.is_valid():
                uniqueID = request.POST["uniqueID"]
                vehicleInfo = getVehicleInfoFromUniqueID(
                    register_contract, uniqueID)
                vehicleInfo = vehicleInfo["data"]
                for i in range(len(vehicleInfo) - 2):
                    vehicleInfoDict[vehicleInfoVars[i]] = vehicleInfo[i]
                owners = getOwnersFromUniqueID(
                    register_contract, uniqueID)["data"]
                prevOwnersNum = len(owners) - 1
                return render(
                    request,
                    "show-police-vehicle-info.html",
                    {
                        "vehicleInfoDict": vehicleInfoDict,
                        "prevOwnersNum": prevOwnersNum,
                    },
                )
            else:
                return render(request, "get-uniqueID-input-form.html", {"form": form})
    else:
        uniqueID = id
        vehicleInfo = getVehicleInfoFromUniqueID(register_contract, uniqueID)
        vehicleInfo = vehicleInfo["data"]
        if vehicleInfo[1] == "":
            return redirect("registration:vehicle_noId")
        else:
            for i in range(len(vehicleInfo) - 2):
                vehicleInfoDict[vehicleInfoVars[i]] = vehicleInfo[i]
            owners = getOwnersFromUniqueID(register_contract, uniqueID)["data"]
            prevOwnersNum = len(owners) - 1
            return render(
                request,
                "show-police-vehicle-info.html",
                {
                    "vehicleInfoDict": vehicleInfoDict,
                    "prevOwnersNum": prevOwnersNum,
                },
            )


@login_required(login_url="registration:login")
@user_passes_test(is_police, login_url="registration:login")
def add_fir(request, id):
    if request.method == "GET":
        form = FirForm()
        return render(
            request,
            "add-fir-form.html",
            {
                "form": form,
            },
        )
    else:
        form = FirForm(request.POST)
        if form.is_valid():
            storeFirInfo(
                register_contract,
                str(id),
                request.POST["firNo"],
                request.POST["district"],
                request.POST["year"],
                request.POST["reason"],
            )
            message = "FIR Informtion Added Successfully"
            return render(
                request,
                "police-dashboard.html",
                {"form": form, "message": message},
            )
        else:
            return render(
                request,
                "add-fir-form.html",
                {"form": form},
            )


def all_firs(request, id):
    isCustomer = is_customer(request.user)
    isPolice = is_police(request.user)
    firs = getVehicleInfoFromUniqueID(register_contract, str(id))["data"][-1]
    return render(
        request,
        "show-all-firs.html",
        {"firs": firs, "isCustomer": isCustomer, "isPolice": isPolice},
    )


def fir_details(request, id):
    isCustomer = is_customer(request.user)
    isPolice = is_police(request.user)
    fir = getFirInfoFromFirNo(register_contract, str(id))["data"]
    return render(
        request,
        "show-fir-details.html",
        {"fir": fir, "isCustomer": isCustomer, "isPolice": isPolice},
    )


@login_required(login_url="registration:login")
@user_passes_test(is_rto, login_url="registration:login")
def rto_choose_update(request):
    return render(request, "rto-choose-update.html")


@login_required(login_url="registration:login")
@user_passes_test(is_rto, login_url="registration:login")
def rto_update_vehicle_info_1(request):
    if request.method == "GET":
        form = UniqueIDInputForm()
        return render(request, "get-uniqueID-input-form.html", {"form": form})
    else:
        form = UniqueIDInputForm(request.POST)
        if form.is_valid():
            uniqueID = request.POST["uniqueID"]
            vehicleInfo = getVehicleInfoFromUniqueID(
                register_contract, uniqueID)
            vehicleInfo = vehicleInfo["data"]
            vehicleInfoVars = [
                "exists2",
                "uniqueID",
                "vehicleNo",
                "modelName",
                "vehicleColor",
            ]
            vehicleInfoDict = {}
            for i in range(1, len(vehicleInfo) - 2):
                vehicleInfoDict[vehicleInfoVars[i]] = vehicleInfo[i]
            request.session["vehicleInfoDict"] = vehicleInfoDict
            return redirect("registration:rto_update_vehicle_info_2")
        else:
            return render(request, "get-uniqueID-input-form.html", {"form": form})


@login_required(login_url="registration:login")
@user_passes_test(is_rto, login_url="registration:login")
def rto_update_vehicle_info_2(request):
    vehicleInfoDict = request.session["vehicleInfoDict"]
    if request.method == "GET":
        form = VehicleInfoForm(initial=vehicleInfoDict)
        return render(
            request,
            "rto-update-vehicle-info-form.html",
            {"vehicleInfoDict": vehicleInfoDict, "form": form},
        )
    else:
        form = VehicleInfoForm(request.POST or None)
        if form.is_valid():
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
            message = "Updated Vehicle Information Successfully!"
            return render(
                request,
                "rto-dashboard.html",
                {"message": message},
            )
        else:
            return render(
                request,
                "rto-update-vehicle-info-form.html",
                {"vehicleInfoDict": vehicleInfoDict, "form": form},
            )


@login_required(login_url="registration:login")
@user_passes_test(is_rto, login_url="registration:login")
def rto_update_owner_info_1(request):
    if request.method == "GET":
        form = AadharInputForm()
        return render(request, "get-aadhar-input-form.html", {"form": form})
    else:
        form = AadharInputForm(request.POST)
        if form.is_valid():
            aadhar = request.POST["aadhar"]
            ownerInfo = getOwnerInfoFromAadhar(
                register_contract, aadhar)["data"]
            ownerInfoVars = [
                "exists1",
                "fName",
                "lName",
                "aadhar",
                "dob",
                "userID",
                "email",
                "mobileNo",
                "gender",
            ]
            ownerInfoDict = {}
            for i in range(1, len(ownerInfo) - 2):
                ownerInfoDict[ownerInfoVars[i]] = ownerInfo[i]
            (
                ownerInfoDict["mobileNo"],
                ownerInfoDict["email"],
                ownerInfoDict["gender"],
            ) = ownerInfo[-1]
            request.session["ownerInfoDict"] = ownerInfoDict
            return redirect("registration:rto_update_owner_info_2")
        else:
            return render(request, "get-aadhar-input-form.html", {"form": form})


@login_required(login_url="registration:login")
@user_passes_test(is_rto, login_url="registration:login")
def rto_update_owner_info_2(request):
    ownerInfoDict = request.session["ownerInfoDict"]
    if request.method == "GET":
        form = OwnerInfoForm(initial=ownerInfoDict)
        return render(
            request,
            "rto-update-owner-info-form.html",
            {"ownerInfoDict": ownerInfoDict, "form": form},
        )
    else:
        form = OwnerInfoForm(request.POST or None)
        if form.is_valid():
            aadhar = ownerInfoDict["aadhar"]
            ownerInfoVars = [
                "fName",
                "lName",
                "aadhar",
                "dob",
                "email",
                "mobileNo",
                "gender",
            ]
            newOwnerInfoDict = {}
            for i in range(len(ownerInfoVars)):
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
            message = "Owner Information updated successfully!"
            return render(
                request,
                "rto-dashboard.html",
                {"message": message},
            )
        else:
            return render(
                request,
                "rto-update-owner-info-form.html",
                {"ownerInfoDict": ownerInfoDict, "form": form},
            )


def login(request, id):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form, "id": id})
    else:
        message = ""
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
                    return redirect("registration:police_dashboard")
                elif is_customer(user) and id == "customer":
                    return redirect("registration:customer_dashboard")
                else:
                    message = "Access Denied!"
                    return render(
                        request,
                        "login.html",
                        {"form": form, "message": message, "id": id},
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
            message = "Invalid Credentials!"
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

@login_required(login_url="registration:login")
@user_passes_test(is_customer, login_url="registration:login")
def change_password(request):
    if request.method == "GET":
        form = change_password_form()
        return render(request, "change_password.html", {"form": form})
    else:
        form = change_password_form(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data["old_password"]
            new_password = form.cleaned_data["password"]
            user = request.user
            if user.check_password(old_password):
                try:
                    validate_password(new_password)
                    if user.check_password(new_password):
                        form.add_error(
                            "password", "Password entered is same as the previous one!"
                        )
                    else:
                        user.set_password(new_password)
                        our_user = Customer.objects.get(user_id=request.user.id)
                        our_user.password_changed = True
                        our_user.first_password = ""
                        our_user.save()
                        user.save()
                        logout(request)
                        return redirect("registration:password_changed")
                except ValidationError as e:
                    form.add_error("password", e)
            else:
                form.add_error("old_password", "Incorrect Password")
        return render(request, "change_password.html", {"form": form})


def password_changed(request):
    return render(request, "password_changed.html", {})