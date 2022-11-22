
from django.urls import path

from . import views

app_name = 'auth0m'
urlpatterns = [
    path("profile_update", views.profile_update, name="profile_update"),
]