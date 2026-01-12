# authentication.py
from datetime import timedelta

from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.authentication.models import AuthToken, Session

User = get_user_model()


class BearerTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        from config.core.api_exceptions import APIValidation

        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not auth_header.startswith('Bearer ') or request.path.startswith('/auth/token/'):
            return None

        token = auth_header[7:].strip()

        try:
            auth_token = AuthToken.objects.get(id=token)
            if auth_token.is_expired():
                # auth_token.delete()
                raise APIValidation('Token expired', status_code=401)

            # Verify session
            try:
                session = Session.objects.get(access_token_id=auth_token.id)
            except Session.DoesNotExist:
                # auth_token.delete()
                raise APIValidation('Session invalid', status_code=401)

            session.expire_date = timezone.now() + timedelta(days=1)
            session.save()
            return auth_token.user, auth_token

        except AuthToken.DoesNotExist:
            raise APIValidation('Invalid token', status_code=401)
