
from django.urls import path

from . import views

app_name = 'auth0'
urlpatterns = [
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("callback", views.callback, name="callback"),
    path("change_email", views.trigger_change_email, name="trigger_change_email")
]