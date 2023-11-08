import configparser
from datetime import time

import requests

from ..common.models.token import Token


class LinkedInToken(Token):
    def __init__(self, scope:str, value:str, expiration_timestamp:str, refresh_value:str, refresh_expiration_timestamp:str):
        super().__init__(value=value, expiration_timestamp=expiration_timestamp)
        self.__refresh_token = Token(value=refresh_value, expiration_timestamp=refresh_expiration_timestamp)
        self.__scope = scope

    @property
    def refresh_token(self) -> Token:
        return self.__refresh_token

    @property
    def scope(self) -> Token:
        return self.__scope

    @property
    def is_refreshable(self) -> bool:
        return self.is_expired and self.refresh_token.is_expired

    @property
    def is_valid(self):
        url = 'https://api.linkedin.com/rest/adAccounts?q=search&search=(status:(values:List(ACTIVE)))'
        headers = {
            'Authorization': f'Bearer {self.value}',
            'Linkedin-Version': '202305',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        response = requests.get(url, headers=headers)
        return response.status_code == 200

    def to_config_ini(self):
        config = configparser.ConfigParser()
        config['LinkedIn Token']= {
            'scope': self.scope,
            'value': self.value,
            'expiration_timestamp': self.expiration_timestamp,
            'expires_at': self.expires_at
        }
        config['LinkedIn Refresh Token'] ={
            'value': self.refresh_token.value,
            'expiration_timestamp': self.refresh_token.expiration_timestamp,
            'expires_at': self.refresh_token.expires_at
        }
        return config

    def __repr__(self):
        return f"LinkedInToken(value='{self.value}', expires_at='{self.expiration_timestamp}', refresh_token='{self.refresh_token.value}', refresh_token_expires_at='{self.refresh_token.expiration_timestamp}')"

    def refresh_access_token(self, client_id, client_secret):
        url = 'https://www.linkedin.com/oauth/v2/accessToken'

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token.value,
            'client_id': client_id,
            'client_secret': client_secret
        }

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            response_data = response.json()

            self.value = str(response_data['access_token'])
            self.expiration_timestamp = float(time.time() + response_data['expires_in'])
            self.refresh_token.value = str(response_data['refresh_token'])
            self.refresh_token.expiration_timestamp = float(time.time() + response_data['refresh_token_expires_in'])

        else:
            raise Exception(f'Failed to refresh access token. Status code: {response.status_code}')
