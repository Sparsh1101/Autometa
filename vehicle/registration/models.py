import os
from posixpath import splitext
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET, SET_NULL
from shared.encryption import EncryptionHelper

# Create your models here.
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.BinaryField()
    lname = models.BinaryField()
    aadhar = models.BinaryField(null=True)
    email = models.BinaryField(null=True)
    mobile_no = models.BinaryField(null=True)
    gender = models.BinaryField()
    dob = models.BinaryField()

    def __str__(self):
        encryptionHelper = EncryptionHelper()
        return encryptionHelper.decrypt(self.fname)