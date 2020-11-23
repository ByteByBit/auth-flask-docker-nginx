import os
from time import time

import jwt
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
from flask import make_response

from src.config import SocialConfig


class UserToken:
    ''' Class to generate & validate user tokens. '''

    @staticmethod
    def create(email: str, expires: int = 600):
        '''Get token.'''

        return jwt.encode(
            {
                'email': email,
                'exp': time() + expires
            },
            key=os.getenv('SECRET_KEY')
        )

    @staticmethod
    def verify(token: str):
        ''' Verify token.'''

        try:
            token = jwt.decode(token, key=os.getenv('SECRET_KEY'))

            # Expired.
            if token['exp'] < time():
                return False

            email = token['email']

        except Exception as e:
            print(e)
            return False

        return email


class SocialLogin(SocialConfig):
    '''Social media login.'''

    def __init__(self, provider: str):

        self.config = SocialConfig().CONFIG
        self.key = SocialConfig().SECRET_KEY
        self.provider = provider
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    def login(self, request):

        authomatic = Authomatic(
            self.config, self.key, report_errors=True)

        response = make_response()
        result = authomatic.login(WerkzeugAdapter(
            request, response),
            self.provider)
            
        return response, result
