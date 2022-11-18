import json
from django.shortcuts import render


def universal_login(request):
    return render(
        request,
        "authenticate/universal_login.html",
    )