import json
import requests
from django.shortcuts import (
    render,
    redirect,
)
from django.urls import reverse
from core.types import PROFILE_STATES


def universal_login(request):
    if request.user.is_authenticated:
        userinfo = request.session['userinfo']
        token = request.session['token']
    else:
        userinfo = None
        token = None
    return render(
        request,
        "authenticate/universal_login.html",
        context={
            "session": request.session.get("user"),
            "userinfo": json.dumps(userinfo, indent=4),
            "token": json.dumps(token, indent=4),
        },
    )


def change_password(request):
    password_change_email_sent = False
    response = ''
    if request.GET.get('email', '') == 'sent':
        password_change_email_sent = True
        response = request.GET.get('response', '')

    if request.user.is_authenticated:
        userinfo = request.session['userinfo']
        token = request.session['token']
    else:
        userinfo = None
        token = None
    return render(
        request,
        "authenticate/change_password.html",
        context={
            "session": request.session.get("user"),
            "sent": password_change_email_sent,
            "response": response,
            "userinfo": json.dumps(userinfo, indent=4),
            "token": json.dumps(token, indent=4),
        },
    )


def update_profile(request):
    return render(
        request,
        "authenticate/update_profile.html",
        context={},
    )


def profile_updated(request):
    response = request.GET.get('response', '')

    return render(
        request,
        "authenticate/profile_updated.html",
        context={
            "session": request.session.get("user"),
            "response": response,
        },
    )


def login_check(request):
    userinfo = request.session['userinfo']
    # print(type(userinfo)) # type: dict
    # print(userinfo)

    if userinfo.get("profile_state") == PROFILE_STATES.NEW.value:
        return redirect(request.build_absolute_uri(reverse("authenticate:update_profile")))

    return redirect(request.build_absolute_uri(reverse("core:index")))


def new_universal_login(request):
    if request.user.is_authenticated:
        userinfo = request.session['userinfo']
        token = request.session['token']
    else:
        userinfo = None
        token = None
    return render(
        request,
        "authenticate/new_universal_login.html",
        context={
            "session": request.session.get("user"),
            "userinfo": json.dumps(userinfo, indent=4),
            "token": json.dumps(token, indent=4),
        },
    )
