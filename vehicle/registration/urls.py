from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("rto", views.rto_dashboard, name="rto_dashboard"),
    path("rto/register", views.register, name="register"),
    path("rto/owner", views.rto_owner, name="rto_owner"),
    path("loggedIn", views.loggedIn, name="loggedIn"),
    
]
