from rest_framework import authentication, exceptions
from django.contrib.auth.models import AnonymousUser
import os

class AuthenticatedAPIUser(AnonymousUser):
    @property
    def is_authenticated(self):
        return True

class APIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('X-API-Key')
        expected_key = os.getenv('API_KEY')

        if not expected_key:
            return None

        if api_key == expected_key:
            return (AuthenticatedAPIUser(), None)
        
        return None
