import os
from posixpath import splitext
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET, SET_NULL
import qrcode


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_password = models.CharField(max_length=225, default="")
    password_changed = models.BooleanField(default=True)