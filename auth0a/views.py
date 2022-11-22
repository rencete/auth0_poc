import urllib
import nanoid
from auth0.v3.authentication import Database, GetToken, Users
# from auth0.v3.authentication import Logout
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from urllib.parse import quote_plus, urlencode


domain = settings.AUTH0_DOMAIN
client_id = settings.AUTH0_CLIENT_ID
client_secret = settings.AUTH0_CLIENT_SECRET


def login(request):
    state = nanoid.generate()
    request.session['state'] = state
    # print(state)

    scope = 'openid profile email'

    return redirect(
        f"https://{domain}/authorize?"
        + urlencode(
            {
                "client_id": client_id,
                "response_type": "code",
                "scope": scope,
                "state": state,
                "redirect_uri": request.build_absolute_uri(reverse("auth0a:callback")),
            },
            quote_via=quote_plus,
        ),
    )


def callback(request):
    code = request.GET.get('code', '')
    # print(code)
    current_state = request.GET.get('state', '')
    # print(current_state)
    previous_state = request.session['state']
    if current_state == '' or previous_state == '' or current_state != previous_state:
        # invalid state value
        print(
            f'Mismatch of state values, previous={previous_state}, current={current_state}')
        # redirect to logout just in case
        return redirect(request.build_absolute_uri(reverse("auth0a:logout")))

    client = GetToken(domain)
    response = client.authorization_code(
        client_id=client_id,
        client_secret=client_secret,
        code=code,
        redirect_uri=request.build_absolute_uri(reverse("auth0a:callback")),
    )
    # print(response)

    request.session['token_response'] = response
    access_token = response.get('access_token')
    request.session['token'] = access_token
    # print(access_token)
    id_token = response.get('id_token')
    # print(id_token)

    # Get the userinfo from the endpoint
    userinfo_client = Users(domain)
    userinfo = userinfo_client.userinfo(access_token)
    request.session['userinfo'] = userinfo
    # print(userinfo)

    if userinfo is not None and userinfo != '':
        email = userinfo.get("email")
        name = userinfo.get("name")
        print(email)
        print(name)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(name, email)
    auth_login(request, user)
    return redirect(request.build_absolute_uri(reverse("core:index")))


def logout(request):
    # client = Logout(domain)
    # response = client.logout(
    #     client_id=client_id,
    #     return_to=request.build_absolute_uri(reverse("core:index")),
    # )
    # # print(response)

    # request.session.clear()

    # return HttpResponse(response)

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
    # token = request.session['token']
    # print(token)
    email = request.session['userinfo'].get('email')
    # print(email)

    database = Database(domain)
    response = database.change_password(
        client_id=client_id,
        email=email,
        connection=settings.AUTH0_DB_NAME,
    )
    # print(response)

    return redirect(reverse("authenticate:change_password") + '?email=sent&response=' + urllib.parse.quote_plus(response))
