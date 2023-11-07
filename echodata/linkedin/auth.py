from urllib.parse import quote_plus, urlencode


# auth.py
def generate_auth_url(client_id, client_secret, redirect_uri):
    params = {
                'response_type': 'code',
                'client_id': client_id,
                'redirect_uri': redirect_uri,
                'state': None,
                'scope': 'r_ads_reporting rw_ads r_liteprofile r_emailaddress w_member_social'
            }
    _authorization_url = f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params, quote_via=quote_plus)}"
    return _authorization_url



