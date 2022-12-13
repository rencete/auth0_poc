import json
import base64
from django.shortcuts import (
    render,
    redirect,
)
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from core.types import PROFILE_STATES
from .utils import is_mfa


@login_required
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


@login_required
def change_password(request):
    userinfo = request.session['userinfo']
    if not is_mfa(userinfo):
        return redirect(request.build_absolute_uri(reverse("authenticate:require_step_up")))

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


@login_required
def update_profile(request):
    return render(
        request,
        "authenticate/update_profile.html",
        context={},
    )


@login_required
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


@login_required
def check_profile_on_login(request):
    userinfo = request.session['userinfo']
    # print(type(userinfo)) # type: dict
    # print(userinfo)

    if userinfo.get("profile_state") == PROFILE_STATES.BASIC.value:
        return redirect(request.build_absolute_uri(reverse("authenticate:update_profile")))

    return redirect(request.build_absolute_uri(reverse("core:index")))


@login_required
def require_step_up(request):
    requesting_page = request.GET.get(
        'next', request.build_absolute_uri(reverse("core:index")))
    return render(
        request,
        "authenticate/require_step_up.html",
        context={
            "page": requesting_page,
        },
    )


def basic_profile(request):
    token=request.GET.get('token')
    state=request.GET.get('state')

    if token:
        request.session['profile_token'] = token
    if state:
        request.session['profile_state'] = state

    return render(
        request,
        "authenticate/basic_profile.html",
        context={},
    )


def answer_security_question(request):
    token=request.GET.get('token')
    state=request.GET.get('state')

    # Get the number of attempts for display
    payload_b64 = (token.split('.')[1]).encode('ascii') + b'=='
    # print(payload_b64)
    payload = json.loads(base64.b64decode(payload_b64))
    # print(payload)

    if token:
        request.session['profile_token'] = token
    if state:
        request.session['profile_state'] = state

    return render(
        request,
        "authenticate/answer_security_question.html",
        context={
            "attempt": payload.get('attempts', 0) + 1,
        },
    )


def login_error(request):
    error_code = request.session['error_code']
    error_description = request.session['error_description']

    # clear session to effectively logout and start from scratch
    request.session.clear()

    return render(
        request,
        "authenticate/login_error.html",
        context={
            "session": request.session.get("user"),
            "error": error_code,
            "description": error_description,
        },
    )


@login_required
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
