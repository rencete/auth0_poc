
from django.urls import path

from . import views

app_name = 'auth0a'
urlpatterns = [
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("callback", views.callback, name="callback"),
    path("change_email", views.trigger_change_email, name="trigger_change_email"),
    path("new_login", views.new_login, name="new_login"),
    path("new_callback", views.new_callback, name="new_callback"),
    path("new_logout", views.new_logout, name="new_logout"),
]