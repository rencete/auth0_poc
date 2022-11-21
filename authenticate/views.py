import json
from django.shortcuts import render


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
