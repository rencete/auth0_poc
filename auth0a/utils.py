from django.conf import settings
from auth0.v3.authentication import (
    Users,
)


domain = settings.AUTH0_DOMAIN
client_id = settings.AUTH0_CLIENT_ID
client_secret = settings.AUTH0_CLIENT_SECRET


def get_userinfo(access_token):
    userinfo_client = Users(domain)
    userinfo = userinfo_client.userinfo(access_token)
    print("here")
    print(type(userinfo)) # type: dict
    print(userinfo)

    return userinfo