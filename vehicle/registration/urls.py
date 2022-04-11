from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),

    path("rto", views.rto_dashboard, name="rto_dashboard"),

    path("rto/check-register", views.rto_check_register, name="rto_check_register"),
    path("rto/register", views.rto_register, name="rto_register"),

    path("rto/choose-update", views.rto_choose_update, name="rto_choose_update"),
    path("rto/update-vehicle-info-1", views.rto_update_vehicle_info_1, name="rto_update_vehicle_info_1"),
    path("rto/update-owner-info-1", views.rto_update_owner_info_1, name="rto_update_owner_info_1"),
    path("rto/update-vehicle-info-2", views.rto_update_vehicle_info_2, name="rto_update_vehicle_info_2"),
    path("rto/update-owner-info-2", views.rto_update_owner_info_2, name="rto_update_owner_info_2"),

    path("rto/owner", views.rto_owner, name="rto_owner"),
    
    path("loggedIn", views.loggedIn, name="loggedIn"),
    path("rtologin", views.rtologin, name="login-rto"),
    path("customerlogin", views.customerlogin, name="login-customer"),
    
]
