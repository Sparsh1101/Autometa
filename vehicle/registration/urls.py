from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("rto", views.rto_dashboard, name="rto_dashboard"),
    path("rto/check-register", views.check_register, name="check_register"),
    path("rto/register", views.register, name="register"),
    path("rto/owner", views.rto_owner, name="rto_owner"),
    path("loggedIn", views.loggedIn, name="loggedIn"),
    path("rtologin", views.rtologin, name="login-rto"),
    path("customerlogin", views.customerlogin, name="login-customer"),
    
]
