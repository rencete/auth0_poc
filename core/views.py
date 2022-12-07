import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    # print("keys: " + ' '.join(request.session.keys()))
    # print("items: ")
    # for item in request.session.items():
    #     print(item)
    if request.user.is_authenticated:
        userinfo = request.session['userinfo']
        token = request.session['token']
        token_response = request.session['token_response']
    else:
        userinfo = None
        token = None
        token_response = None
    return render(
        request,
        "core/index.html",
        context={
            "session": request.session.get("user"),
            "userinfo": json.dumps(userinfo, indent=4),
            "token": json.dumps(token, indent=4),
            "token_response": json.dumps(token_response, indent=4),
        },
    )


def cover(request):
    # Redirect to dashboard when already logged in
    if request.user.is_authenticated:
        return redirect(request.build_absolute_uri(reverse("core:index")));

    return render(
        request,
        "core/cover.html",
    )
