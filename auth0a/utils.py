from django.conf import settings
from auth0.v3.authentication import (
    Users,
    token_verifier
)
from auth0.v3.authentication.token_verifier import (
    SymmetricSignatureVerifier,
    TokenVerifier
)


domain = settings.AUTH0_DOMAIN
client_id = settings.AUTH0_CLIENT_ID
client_secret = settings.AUTH0_CLIENT_SECRET


def get_userinfo(access_token):
    userinfo_client = Users(domain)
    userinfo = userinfo_client.userinfo(access_token)
    # print(type(userinfo)) # type: dict
    # print(userinfo)

    return userinfo


def verify_token_symmetric(secret, issuer, audience, token):
    symmetric_verifier = SymmetricSignatureVerifier(secret)
    token_verifier = TokenVerifier(
        symmetric_verifier,
        issuer,
        audience,
    )
    payload = token_verifier.verify(token)
    return payload