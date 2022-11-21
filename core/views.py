import json
from django.shortcuts import render


def index(request):
    # print("keys: " + ' '.join(request.session.keys()))
    # print("items: ")
    # for item in request.session.items():
    #     print(item)
    if request.user.is_authenticated:
        userinfo = request.session['userinfo']
        token = request.session['token']
    else:
        userinfo = None
        token = None
    return render(
        request,
        "core/index.html",
        context={
            "session": request.session.get("user"),
            "userinfo": json.dumps(userinfo, indent=4),
            "token": json.dumps(token, indent=4),
        },
    )


def cover(request):
    return render(
        request,
        "core/cover.html",
    )
