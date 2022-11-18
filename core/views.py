import json
from django.shortcuts import render


def index(request):
    if request.user.is_authenticated:
        pretty = {
            "user": request.user.username,
            "password": request.user.password,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }
    else:
        pretty = None
    return render(
        request,
        "core/index.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(pretty, indent=4),
        },
    )


def cover(request):
    return render(
        request,
        "core/cover.html",
    )
