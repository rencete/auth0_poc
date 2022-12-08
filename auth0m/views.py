import re
import jwt
import base64
import hashlib
import datetime
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from auth0.v3.authentication import GetToken
from auth0.v3.management import Users
from urllib.parse import quote_plus, urlencode
from core.types import PROFILE_STATES
from auth0a.utils import verify_token_symmetric


domain = settings.AUTH0_DOMAIN
client_id = settings.AUTH0_NON_INTERACTIVE_CLIENT_ID
client_secret = settings.AUTH0_NON_INTERACTIVE_CLIENT_SECRET
audience = f"https://{domain}/api/v2/"


def profile_update(request):
    if request.method == 'POST':
        # Get parameters
        language = request.POST.get("preferredLanguageRadioOptions")
        address = request.POST.get("streetAddress")
        city = request.POST.get("city")
        post_code = request.POST.get("postalCode")
        province = request.POST.get("province")
        phone_number = request.POST.get("phoneNumber")
        phone_number = '+1' + re.sub("[^0-9]", "", phone_number)
        birthday = request.POST.get("birthday")
        # print(language)
        # print(address)
        # print(city)
        # print(post_code)
        # print(province)
        # print(phone_number)
        # print(birthday)

        userinfo = request.session['userinfo']
        if userinfo.get("profile_state") == PROFILE_STATES.BASIC.value:
            # Update app_metadata so that no longer forwarded to update profile on login
            app_metadata = {
                "profile_state": PROFILE_STATES.UPDATED.value,
            }
        else:
            app_metadata = {}

        user_metadata = {
            "preferred_language": language if language else None,
            "phone_number": phone_number if (phone_number and phone_number != "+1") else None,
            "birthday": birthday if birthday else None,
            "address": {
                "street_address": address if address else None,
                "city": city if city else None,
                "province": province if province else None,
                "postal_code": post_code if post_code else None,
            }
        }

        update_user_data = {
            "user_metadata": user_metadata,
            "app_metadata": app_metadata,
        }

        get_token = GetToken(domain)
        token = get_token.client_credentials(
            client_id=client_id, client_secret=client_secret, audience=audience)
        # print(token)
        mgmt_api_token = token['access_token']
        # print(mgmt_api_token)

        user_id = request.session['userinfo'].get('sub')
        # print(user_id)

        users = Users(domain, mgmt_api_token)
        response = users.update(user_id, update_user_data)
        # print(type(response))
        # print(response)

        # User information may have been updated
        # Update the userinfo based from response
        updated_userinfo = update_userinfo_from_user(userinfo, response)
        # print(updated_userinfo)
        request.session['userinfo'] = updated_userinfo

        return redirect(
            request.build_absolute_uri(reverse("authenticate:profile_updated"))
            + '?'
            + urlencode(
                {
                    "response": response,
                },
                quote_via=quote_plus,
            ),
        )
    else:
        return redirect(request.build_absolute_uri(reverse("authenticate:update_profile")))


def update_userinfo_from_user(previous_userinfo, user_details):
    updated_userinfo = previous_userinfo

    # handle profile_state
    if user_details.get('app_metadata') and user_details.get('app_metadata').get('profile_state'):
        updated_userinfo['profile_state'] = user_details['app_metadata']['profile_state']

    # handle user_metadata
    if user_details.get('user_metadata'):
        updated_userinfo['user_metadata'] = user_details['user_metadata']

    return updated_userinfo


def basic_profile_update(request):
    if request.method == 'POST':
        # Get parameters
        given_name = request.POST.get("givenName")
        family_name = request.POST.get("familyName")
        province = request.POST.get("province")
        security_answer = request.POST.get("securityAnswer")
        # print(given_name)
        # print(family_name)
        # print(province)
        # print(security_answer)

        hashed_answer = base64.b64encode(hashlib.sha256(
            security_answer.encode('ascii')).digest()).decode('ascii')
        # print(hashed_answer)

        profile_data = {
            "given_name": given_name,
            "family_name": family_name,
            "user_metadata": {
                "province": province,
                "security_answer": hashed_answer,
            }
        }

        # Retrieve information sent by Auth0 from session
        auth0_token = request.session['profile_token']
        state = request.session['profile_state']
        # Delete information sent by Auth0 from session
        del request.session['profile_token']
        del request.session['profile_state']

        # Need the user_id from Auth0 as user is not yet logged in
        auth0_payload_token = verify_token_symmetric(
            settings.HS256_SHARED_SECRET,
            settings.AUTH0_DOMAIN,
            settings.AUTH0_CLIENT_ID,
            auth0_token,
        )
        user_id = auth0_payload_token.get('sub')
        # print(user_id)

        get_token = GetToken(domain)
        mgmt_token = get_token.client_credentials(
            client_id=client_id, client_secret=client_secret, audience=audience)
        # print(token)
        mgmt_api_token = mgmt_token['access_token']
        # print(mgmt_api_token)

        users = Users(domain, mgmt_api_token)
        response = users.update(user_id, profile_data)
        # print(type(response))
        # print(response)

        exp = datetime.datetime.now() + datetime.timedelta(minutes=5)
        exp = int(exp.timestamp())
        client_payload = {
            "sub": user_id,
            "iss": settings.AUTH0_APP_NAME,
            "exp": exp,
            "state": state,
            "aud": settings.AUTH0_DOMAIN, # Not in documentation but mandatory to be included. Value does not seem to be checked.
            "iat": int(datetime.datetime.now().timestamp()), # Not in documentation but mandatory to be included
            # Add additional fields below
            "updated": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        }
        client_payload_token = jwt.encode(
            payload=client_payload,
            key=settings.HS256_SHARED_SECRET
        )
        print(client_payload_token)

        query_params = {
            "state": state,
            "token": client_payload_token,
        }

        return redirect(
            f"https://{domain}/continue?"
            + urlencode(
                query_params,
                quote_via=quote_plus,
            ),
        )
    else:
        return redirect(request.build_absolute_uri(reverse("authenticate:basic_profile")))
