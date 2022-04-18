from django.urls import path
from . import views

app_name = "registration"

urlpatterns = [
    path("", views.index, name="index"),

    path("rto", views.rto_dashboard, name="rto_dashboard"),
    path("customer", views.customer_dashboard, name="customer_dashboard"),
    path("police", views.police_dashboard, name="police_dashboard"),

    path("rto/check-register", views.rto_check_register, name="rto_check_register"),
    path("rto/register", views.rto_register, name="rto_register"),

    path("rto/choose-update", views.rto_choose_update, name="rto_choose_update"),
    path("rto/update-vehicle-info-1", views.rto_update_vehicle_info_1, name="rto_update_vehicle_info_1"),
    path("rto/update-owner-info-1", views.rto_update_owner_info_1, name="rto_update_owner_info_1"),
    path("rto/update-vehicle-info-2", views.rto_update_vehicle_info_2, name="rto_update_vehicle_info_2"),
    path("rto/update-owner-info-2", views.rto_update_owner_info_2, name="rto_update_owner_info_2"),

    path("owner", views.owner, name="owner_noId"),
    path("rto/owner/<str:id>", views.owner, name="owner"),
    path("owner/vehicles/<str:id>", views.owner_vehicles, name="owner_vehicles"),
    path("vehicle", views.vehicle, name="vehicle_noId"),
    path("vehicle/<str:id>", views.vehicle, name="vehicle"),
    path("vehicle/owners/<str:id>", views.vehicle_owners, name="vehicle_owners"),

    path("customer-profile", views.customer_profile, name="customer_profile"),
    path("login/<str:id>", views.login, name="login"),
    path("logout", views.logoutU, name="logout"),
    
    
]
