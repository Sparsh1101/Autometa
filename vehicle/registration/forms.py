from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm
from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from .models import *
from .helper_functions import *
from django.conf import settings

# Create your forms here.
class UserInfoForm(forms.ModelForm):
    email = forms.EmailField(
            required=True,
        )
    fname = forms.CharField(
            max_length=50,
            label="First Name",
        )
    lname = forms.CharField(
            max_length=50,
            label="Last Name",
        )
    # dob = forms.DateField(
    #         widget=DatePickerInput(format="%d/%m/%Y"),
    #         input_formats=settings.DATE_INPUT_FORMATS,
    #         label="Date of Birth",
    #     )
    mobile_no = forms.CharField(
            required=True,
            max_length=10,
            label="Mobile Number",
        )
    GENDER_CHOICES = [("Male", "Male"), ("Female", "Female"), ("Other", "Other")]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    aadhar = forms.CharField(
    max_length=14,
    label="Aadhar Number",
    required=True,
    widget=forms.TextInput(attrs={"onkeyup": "addSpace(this)"}),
    )
    class Meta:
        model = UserInfo
        fields = ["fname", "lname","aadhar","email","mobile_no","gender","dob",]
        labels = {'fname': "First Name", "lname": "Last Name","aadhar": "Aadhar Number","email": "E-mail","mobile_no": "Mobile Number","gender":"Gender","dob":"Date of birth"}

# Create your forms here.
class VehicleInfoForm(forms.ModelForm):
    uniqueID = forms.CharField(
            max_length=50,
            label="Unique ID",
        )
    vehicleNo = forms.CharField(
            max_length=50,
            label="Vehicle No.",
        )
    modelName = forms.CharField(
            max_length=50,
            label="Model Name",
        )
    vehicleColor = forms.CharField(
            max_length=50,
            label="Vehicle Color",
        )
    class Meta:
        model = VehicleInfo
        fields = ["uniqueID", "vehicleNo", "modelName", "vehicleColor"]
