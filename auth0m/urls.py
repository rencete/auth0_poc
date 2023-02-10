
from django.urls import path

from . import views

app_name = 'auth0m'
urlpatterns = [
    path("profile_update", views.profile_update, name="profile_update"),
    path("basic_profile_update", views.basic_profile_update, name="basic_profile_update"),
    path("check_security_answer", views.check_security_answer, name="check_security_answer"),
    path("delete_user_final", views.delete_user, name="delete_user"),
]