from django import forms
from .models import *
from django.conf import settings
from .helper_functions import *
from .deploy import *


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label="Username",
    )
    password = forms.CharField(
        max_length=100,
        label="Password",
        widget=forms.PasswordInput,
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username == None:
            raise forms.ValidationError(
                {"district": "Please Enter a username"})
        if password == None:
            raise forms.ValidationError({"year": "Please Enter a Password"})
        return cleaned_data


class FirForm(forms.Form):
    firNo = forms.CharField(
        max_length=10,
        label="FIR Number",
    )
    district = forms.CharField(
        max_length=50,
        label="District",
    )
    year = forms.CharField(
        max_length=4,
        min_length=4,
        label="Year",
    )
    reason = forms.CharField(
        max_length=100,
        label="Reason",
    )

    def clean(self):
        cleaned_data = super().clean()
        firNo = cleaned_data.get("firNo")
        district = cleaned_data.get("district")
        year = cleaned_data.get("year")
        reason = cleaned_data.get("reason")
        if (firNo == None) or (not valid_firNo(firNo)):
            raise forms.ValidationError(
                {"firNo": "Please Enter a valid value"})
        if getFirInfoFromFirNo(register_contract, firNo)["data"][0] != "":
            raise forms.ValidationError(
                {"firNo": "FIR with this FIR Number already exists"}
            )
        if (district == None) or (not valid_text(district)):
            raise forms.ValidationError(
                {"district": "Please Enter a valid value"})
        if (year == None) or (not valid_year(year)):
            raise forms.ValidationError({"year": "Please Enter a valid value"})
        if reason == None:
            raise forms.ValidationError(
                {"reason": "Please Enter a valid value"})
        return cleaned_data


class CheckRegisterForm(forms.Form):
    uniqueID = forms.CharField(
        max_length=17,
        min_length=17,
        label="Vehicle Identification Number (VIN)",
    )
    aadhar = forms.CharField(
        max_length=12,
        min_length=12,
        label="Aadhar Number",
    )

    def clean(self):
        cleaned_data = super().clean()
        uniqueID = cleaned_data.get("uniqueID")
        aadhar = cleaned_data.get("aadhar")
        if (uniqueID == None) or (not valid_uniqueID(uniqueID)):
            raise forms.ValidationError(
                {"uniqueID": "Please Enter a valid value"})
        if (aadhar == None) or (not valid_aadhar(aadhar)):
            raise forms.ValidationError(
                {"aadhar": "Please Enter a valid value"})
        return cleaned_data


class DateInput(forms.DateInput):
    input_type = "date"


class RegisterForm(forms.Form):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    COLOR_CHOICES = [
        ("White", "White"),
        ("Black", "Black"),
        ("Gray", "Gray"),
        ("Silver", "Silver"),
        ("Red", "Red"),
        ("Blue", "Blue"),
        ("Brown", "Brown"),
        ("Green", "Green"),
        ("Beige", "Beige"),
        ("Orange", "Orange"),
        ("Gold", "Gold"),
        ("Yellow", "Yellow"),
        ("Purple", "Purple"),
    ]

    uniqueID = forms.CharField(
        max_length=17,
        min_length=17,
        label="Vehicle Identification Number (VIN)",
        help_text="This is the chasis number of your vehicle",
        required=False,
    )
    vehicleNo = forms.CharField(
        max_length=11,
        label="Vehicle Registration Number (VRN)",
        help_text="This is the number on your vehicle's number plate",
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    modelName = forms.CharField(
        max_length=50,
        label="Vehicle Model Name",
    )
    vehicleColor = forms.CharField(
        label="Vehicle Color", widget=forms.Select(choices=COLOR_CHOICES)
    )
    fName = forms.CharField(
        max_length=50,
        label="First Name",
    )
    lName = forms.CharField(
        max_length=50,
        label="Last Name",
    )
    email = forms.EmailField(label="Email ID")
    aadhar = forms.CharField(
        max_length=12,
        min_length=12,
        label="Aadhar Number",
        required=False,
    )
    dob = forms.DateField(
        widget=DateInput(attrs={"type": "date"}),
        input_formats=settings.DATE_INPUT_FORMATS,
        label="Date Of Birth",
        help_text="User must be an adult",
    )
    mobileNo = forms.CharField(
        max_length=10,
        label="Mobile Number",
    )
    gender = forms.CharField(
        label="Gender", widget=forms.Select(choices=GENDER_CHOICES)
    )

    def clean(self):
        cleaned_data = super().clean()
        vehicleNo = cleaned_data.get("vehicleNo")
        modelName = cleaned_data.get("modelName")
        fName = cleaned_data.get("fName")
        lName = cleaned_data.get("lName")
        email = cleaned_data.get("email")
        dob = cleaned_data.get("dob")
        mobileNo = cleaned_data.get("mobileNo")
        if (vehicleNo == None) or (not valid_vehicleNo(vehicleNo)):
            raise forms.ValidationError(
                {"vehicleNo": "Please Enter a valid value"})
        if (modelName == None) or (not valid_alphanumeric(modelName)):
            raise forms.ValidationError(
                {"modelName": "Please Enter a valid value"})
        if (fName == None) or (not valid_text(fName)):
            raise forms.ValidationError({"fName": "Invalid First Name."})
        if (lName == None) or (not valid_text(lName)):
            raise forms.ValidationError({"lName": "Invalid Last Name."})
        if (email != "") and (not valid_email(email)):
            raise forms.ValidationError({"email": "Invalid Email."})
        if dob != None and not valid_adult(str(dob)):
            raise forms.ValidationError({"dob": "Invalid Date of Birth."})
        if (mobileNo == None) or (not valid_mobileNo(mobileNo)):
            raise forms.ValidationError({"mobileNo": "Invalid Mobile Number."})
        return cleaned_data


class UniqueIDInputForm(forms.Form):
    uniqueID = forms.CharField(
        max_length=17,
        min_length=17,
        label="Vehicle Identification Number (VIN)",
    )

    def clean(self):
        cleaned_data = super().clean()
        uniqueID = cleaned_data.get("uniqueID")
        if (uniqueID == None) or (not valid_uniqueID(uniqueID)):
            raise forms.ValidationError(
                {"uniqueID": "Please Enter a valid value"})
        if getVehicleInfoFromUniqueID(register_contract, uniqueID)["data"][0] == False:
            raise forms.ValidationError(
                {"uniqueID": "Vehicle with entered VIN does not exist"}
            )
        return cleaned_data


class AadharInputForm(forms.Form):
    aadhar = forms.CharField(
        max_length=12,
        min_length=12,
        label="Aadhar Number",
    )

    def clean(self):
        cleaned_data = super().clean()
        aadhar = cleaned_data.get("aadhar")
        if (aadhar == None) or (not valid_aadhar(aadhar)):
            raise forms.ValidationError(
                {"aadhar": "Please Enter a valid value"})
        if getOwnerInfoFromAadhar(register_contract, aadhar)["data"][0] == False:
            raise forms.ValidationError(
                {"aadhar": "Owner with entered Aadhar Number does not exist"}
            )
        return cleaned_data


class VehicleInfoForm(forms.Form):
    COLOR_CHOICES = [
        ("White", "White"),
        ("Black", "Black"),
        ("Gray", "Gray"),
        ("Silver", "Silver"),
        ("Red", "Red"),
        ("Blue", "Blue"),
        ("Brown", "Brown"),
        ("Green", "Green"),
        ("Beige", "Beige"),
        ("Orange", "Orange"),
        ("Gold", "Gold"),
        ("Yellow", "Yellow"),
        ("Purple", "Purple"),
    ]

    uniqueID = forms.CharField(
        max_length=17,
        min_length=17,
        label="Vehicle Identification Number (VIN)",
        help_text="This is the chasis number of your vehicle",
        required=False,
    )
    vehicleNo = forms.CharField(
        max_length=11,
        label="Vehicle Registration Number (VRN)",
        help_text="This is the number on your vehicle's number plate",
    )
    modelName = forms.CharField(
        max_length=50,
        label="Vehicle Model Name",
    )
    vehicleColor = forms.CharField(
        label="Vehicle Color", widget=forms.Select(choices=COLOR_CHOICES)
    )

    def clean(self):
        cleaned_data = super().clean()
        vehicleNo = cleaned_data.get("vehicleNo")
        modelName = cleaned_data.get("modelName")
        if (vehicleNo == None) or (not valid_vehicleNo(vehicleNo)):
            raise forms.ValidationError(
                {"vehicleNo": "Please Enter a valid value"})
        if (modelName == None) or (not valid_alphanumeric(modelName)):
            raise forms.ValidationError(
                {"modelName": "Please Enter a valid value"})
        return cleaned_data


class OwnerInfoForm(forms.Form):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    fName = forms.CharField(
        max_length=50,
        label="First Name",
    )
    lName = forms.CharField(
        max_length=50,
        label="Last Name",
    )
    email = forms.EmailField(label="Email ID")
    aadhar = forms.CharField(
        max_length=12,
        min_length=12,
        label="Aadhar Number",
        required=False,
    )
    dob = forms.DateField(
        widget=DateInput(attrs={"type": "date"}),
        input_formats=settings.DATE_INPUT_FORMATS,
        label="Date Of Birth",
        help_text="User must be an adult",
    )
    mobileNo = forms.CharField(
        max_length=10,
        label="Mobile Number",
    )
    gender = forms.CharField(
        label="Gender", widget=forms.Select(choices=GENDER_CHOICES)
    )

    def clean(self):
        cleaned_data = super().clean()
        fName = cleaned_data.get("fName")
        lName = cleaned_data.get("lName")
        email = cleaned_data.get("email")
        dob = cleaned_data.get("dob")
        mobileNo = cleaned_data.get("mobileNo")
        if (fName == None) or (not valid_text(fName)):
            raise forms.ValidationError({"fName": "Invalid First Name."})
        if (lName == None) or (not valid_text(lName)):
            raise forms.ValidationError({"lName": "Invalid Last Name."})
        if (email != "") and (not valid_email(email)):
            raise forms.ValidationError({"email": "Invalid Email."})
        if dob != None and not valid_adult(str(dob)):
            raise forms.ValidationError({"dob": "Invalid Date of Birth."})
        if (mobileNo == None) or (not valid_mobileNo(mobileNo)):
            raise forms.ValidationError({"mobileNo": "Invalid Mobile Number."})
        return cleaned_data
