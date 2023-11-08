import time
from urllib.parse import quote_plus, urlencode

import requests

from .token import LinkedInToken


def generate_auth_url(client_id: str, redirect_uri: str):
    params = {
                'response_type': 'code',
                'client_id': client_id,
                'redirect_uri': redirect_uri,
                'state': None,
                'scope': 'r_ads_reporting r_ads r_liteprofile r_emailaddress'
            }
    _authorization_url = f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params, quote_via=quote_plus)}"
    return _authorization_url

def exchange_code_for_token(client_id: str, client_secret: str, redirect_uri: str, auth_code: str) -> LinkedInToken:
    url = 'https://www.linkedin.com/oauth/v2/accessToken'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return LinkedInToken(scope=str(response.json()['scope']), value=str(response.json()['access_token']), expiration_timestamp=str(time.time() + response.json()['expires_in']), refresh_value=str(response.json()['refresh_token']), refresh_expiration_timestamp=str(time.time() + response.json()['refresh_token_expires_in']))
    else:
        raise Exception(f"Failed to get access token.\nResponse Content:\n{response.content}")

