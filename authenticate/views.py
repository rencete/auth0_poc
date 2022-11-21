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