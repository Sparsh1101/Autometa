import os
from posixpath import splitext
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET, SET_NULL

# Create your models here.
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100, null=True)
    lname = models.CharField(max_length=100, null=True)
    aadhar = models.CharField(max_length=12, null=True)
    email = models.EmailField(max_length=100, null=True)
    mobile_no = models.CharField(max_length=10, null=True)
    gender = models.CharField(max_length=100, null=True)
    dob = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.fname

class VehicleInfo(models.Model):
    uniqueID = models.CharField(max_length=100, null=True)
    vehicleNo = models.CharField(max_length=100, null=True)
    modelName = models.CharField(max_length=12, null=True)
    vehicleColor = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.fname