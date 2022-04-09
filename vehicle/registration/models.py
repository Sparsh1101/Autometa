import os
from posixpath import splitext
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET, SET_NULL

# Create your models here.
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    aadhar = models.CharField(max_length=12)
    email = models.EmailField(max_length=100)
    mobile_no = models.CharField(max_length=10)
    gender = models.CharField(max_length=100)
    dob = models.CharField(max_length=100)

    def __str__(self):
        return self.fname