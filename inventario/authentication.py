from rest_framework import authentication, exceptions
import os

class APIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('X-API-Key')
        expected_key = os.getenv('API_KEY')

        if api_key and expected_key and api_key == expected_key:
            return (None, None)
        return None
