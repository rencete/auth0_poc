from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from auth0.v3.authentication import GetToken
from auth0.v3.management import Users

# from django.contrib.auth.models import User
# from django.contrib.auth import login as auth_login
# from urllib.parse import quote_plus, urlencode

# import http.client
import json
# import 


domain = settings.AUTH0_DOMAIN
client_id = settings.AUTH0_NON_INTERACTIVE_CLIENT_ID
client_secret = settings.AUTH0_NON_INTERACTIVE_CLIENT_SECRET
audience = f"https://{domain}/api/v2/"


def profile_update(request):
    get_token = GetToken(domain)
    token = get_token.client_credentials(client_id=client_id, client_secret=client_secret, audience=audience)
    # print(token)
    mgmt_api_token = token['access_token']
    # print(mgmt_api_token)

    user_id = request.session['userinfo'].get('sub')
    # print(user_id)

    user_metadata = {
        "user_metadata": {
            "profileCode": 1479,
            "addresses": {
                "work_address": "100 Industrial Way",
            }
        }
    }
    print(user_metadata)

    users = Users(domain, mgmt_api_token)
    response = users.update(user_id, user_metadata)
    print(response)

    return redirect(reverse("authenticate:update_profile"))