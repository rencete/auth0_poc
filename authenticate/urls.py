from django.urls import path
from . import views

app_name = 'authenticate'

urlpatterns = [
    path("universal_login", views.universal_login, name="universal_login"),
    path("change_password", views.change_password, name="change_password"),
    path("update_profile", views.update_profile, name="update_profile"),
    path("profile_updated", views.profile_updated, name="profile_updated"),
]