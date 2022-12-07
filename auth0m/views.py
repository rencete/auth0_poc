import re
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from auth0.v3.authentication import GetToken
from auth0.v3.management import Users
from urllib.parse import quote_plus, urlencode
from core.types import PROFILE_STATES


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
        if userinfo.get("profile_state") == PROFILE_STATES.NEW.value:
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
        print(type(response))
        print(response)

        # User information may have been updated
        # Update the userinfo based from response
        updated_userinfo = update_userinfo_from_user(userinfo, response)
        print(updated_userinfo)
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