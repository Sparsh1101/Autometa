from datetime import datetime, date
from enum import unique
from os import name
from .models import *
import re


def is_rto(user):
    return user.groups.filter(name="rto").exists()


def is_police(user):
    return user.groups.filter(name="police").exists()


def is_customer(user):
    return user.groups.filter(name="customer").exists()


def valid_firNo(firNo):
    firNo = str(firNo)
    return re.match("^\d{4}$", firNo)


def valid_text(name):
    name = str(name)
    return re.match("^[a-zA-z ][a-zA-Z' ]*$", name)

def valid_alphanumeric(name):
    name = str(name)
    return re.match("^[a-zA-z0-9 ][a-zA-Z0-9' ]*$", name)

def valid_year(year):
    year = str(year)
    return re.match("^\d{4}$", year) and (year <= str(date.today().year))


def valid_aadhar(aadhar):
    aadhar = str(aadhar)
    return re.match("^\d{12}$", aadhar)

def valid_uniqueID(uniqueID):
    uniqueID = str(uniqueID)
    return re.match("^[a-zA-z0-9]{17}$", uniqueID)

def valid_vehicleNo(vehicleNo):
    vehicleNo = str(vehicleNo)
    return re.match("^[A-Z|a-z]{2}\s?[0-9]{1,2}\s?[A-Z|a-z]{0,3}\s?[0-9]{4}$", vehicleNo)


def valid_dob(dob):
    today = str(date.today())
    student_dob_year = int(dob[:4])
    student_dob_month = int(dob[5:7])
    student_dob_date = int(dob[8:])
    today_year = int(today[:4])
    today_month = int(today[5:7])
    today_date = int(today[8:])
    is_valid = False
    if (today_year - 5 > student_dob_year) or (
        (today_year - 5 == student_dob_year)
        and (
            (today_month > student_dob_month)
            or ((today_month == student_dob_month) and (today_date >= student_dob_date))
        )
    ):
        is_valid = True
    return is_valid


def valid_email(email):
    email = str(email)
    return re.match("^[a-zA-Z0-9_\.\+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-\.]+$", email)


def valid_mobileNo(mobileNo):
    mobileNo = str(mobileNo)
    return re.match("^\d{10}$", mobileNo)

def valid_date(date):
    date_year = int(date[6:])
    date_month = int(date[3:5])
    date_date = int(date[:2])
    try:
        datetime(date_year, date_month, date_date)
        return True
    except:
        return False

def valid_adult(dob):
    today = str(date.today())
    dob_year = int(dob[:4])
    dob_month = int(dob[5:7])
    dob_date = int(dob[8:])
    today_year = int(today[:4])
    today_month = int(today[5:7])
    today_date = int(today[8:])
    is_valid = False
    if (today_year - 18 > dob_year) or (
        (today_year - 18 == dob_year)
        and (
            (today_month > dob_month)
            or ((today_month == dob_month) and (today_date >= dob_date))
        )
    ):
        is_valid = True
    return is_valid

