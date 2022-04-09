from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm
from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from .models import *
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
    dob = forms.DateField(
        widget=DatePickerInput(format="%d/%m/%Y"),
        input_formats=settings.DATE_INPUT_FORMATS,
        label="Date of Birth",
    )
    mobile_no = forms.CharField(
        required=False,
        help_text="Enter 10 digit mobile number.",
        max_length=10,
        label="Mobile Number",
    )
    GENDER_CHOICES = [("Male", "Male"), ("Female", "Female"), ("Other", "Other")]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    aadhar = forms.CharField(
        max_length=14,
        label="Aadhar Number",
        help_text="Aadhar Number is used for password reset.",
        required=False,
        widget=forms.TextInput(attrs={"onkeyup": "addSpace(this)"}),
    )

    class Meta:
        model = UserInfo
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get("dob")
        email = cleaned_data.get("email")
        fname = cleaned_data.get("fname")
        mname = cleaned_data.get("mname")
        lname = cleaned_data.get("lname")
        mobile_no = cleaned_data.get("mobile_no")
        aadhar = cleaned_data.get("aadhar")
        if (aadhar != "") and (not valid_aadhar(aadhar)):
            raise forms.ValidationError({"aadhar": "Invalid Aadhar Number."})
        if dob != None and not valid_adult(str(dob)):
            raise forms.ValidationError({"dob": "User isn't an adult."})
        if (email != "") and (not valid_email(email)):
            raise forms.ValidationError({"email": "Invalid Email."})
        if (fname == None) or (not valid_name(fname)):
            raise forms.ValidationError({"fname": "Invalid First Name."})
        if (mname != "") and (not valid_name(mname)):
            raise forms.ValidationError({"mname": "Invalid Middle Name."})
        if (lname == None) or (not valid_name(lname)):
            raise forms.ValidationError({"lname": "Invalid Last Name."})
        if (mobile_no != "") and (not valid_mobile_no(mobile_no)):
            raise forms.ValidationError({"mobile_no": "Invalid Mobile Number."})
        return cleaned_data
