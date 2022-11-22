from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from urllib.parse import quote_plus, urlencode

import http.client
import json
import urllib


oauth = OAuth()

oauth.register(
    "auth0a",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def login(request):
    return oauth.auth0a.authorize_redirect(
        request, request.build_absolute_uri(reverse("auth0a:callback"))
    )


def callback(request):
    token = oauth.auth0a.authorize_access_token(request)
    request.session['token'] = token
    # print(token)
    userinfo = token.get("userinfo")
    request.session['userinfo'] = userinfo
    # print(userinfo)
    if userinfo is not None:
        email = userinfo.get("email")
        name = userinfo.get("name")
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(name, email)
    auth_login(request, user)
    return redirect(request.build_absolute_uri(reverse("core:index")))


def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("core:index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )


def trigger_change_email(request):
    token = request.session['token'].get('access_token')
    # print(token)
    email = request.session['userinfo'].get('email')
    # print(email)

    conn = http.client.HTTPSConnection(f"{settings.AUTH0_DOMAIN}")
    payload = {
        'client_id': settings.AUTH0_CLIENT_ID,
        'email': email,
        'connection': settings.AUTH0_DB_NAME,
    }
    payload = json.dumps(payload)
    # print(payload)

    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    # print(headers)
    
    conn.request("POST", "/dbconnections/change_password", payload, headers)
    res = conn.getresponse()
    data = res.read()
    # print(data.decode("utf-8"))

    return redirect(reverse("authenticate:change_password") + '?email=sent&response=' + urllib.parse.quote_plus(data.decode("utf-8")))
