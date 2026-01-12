from datetime import timedelta

from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.authentication.models import AuthToken, Session, Role
from apps.authentication.serializers import LoginSerializer, JWTObtainPairSerializer
from config.core.api_exceptions import APIValidation


class InitSessionView(APIView):
    permission_classes = [AllowAny, ]
    """View to initialize a session before login"""

    def get(self, request):
        session = Session.objects.create(expire_date=timezone.now() + timedelta(days=1))

        return Response({
            'session_id': session.id,
            'token_id': None
        }, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [AllowAny, ]

    @staticmethod
    def get_session(session_key):
        try:
            session = Session.objects.get(id=session_key)
            if timezone.now() > session.expire_date:
                token_non_exists = AuthToken.objects.filter(sessions=session_key, expires_at__lt=timezone.now())
                if token_non_exists:
                    session.delete()
                    token_non_exists.delete()
                raise APIValidation('Session expired', status_code=status.HTTP_401_UNAUTHORIZED)
            return session
        except Session.DoesNotExist:
            raise APIValidation('Session does not exist', status_code=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def permissions_by_category(permissions):
        categories = set({i.split('_')[-1] for i in permissions})
        categories = {i: [] for i in categories}
        for permission in permissions:
            category_part = permission.split('_')[-1]
            categories[category_part].append(permission)
        return categories

    @swagger_auto_schema(
        request_body=LoginSerializer,
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                description="Authorization: Bearer <session_id>",
                type=openapi.TYPE_STRING,
                required=False,
            )
        ]
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        session_id = request.headers['Authorization'].split(' ')[-1]
        session = self.get_session(session_id)
        token = AuthToken.create_token(user, session.id)
        session.access_token = token
        session.expire_date = timezone.now() + timedelta(days=1)
        session.save()
        user.last_login = timezone.now()
        user.save()
        permissions = (
            Role.objects
            .filter(users_roles__user=user, users_roles__is_deleted=False)
            .values_list('role_permissions__permission', flat=True)
        )
        return Response({
            'session_id': session.id,
            'access_token': str(token.id),
            'token_expires_at': token.expires_at,
            'session_expires_at': session.expire_date,
            'user_id': user.id,
            'username': user.username,
            'permissions': permissions,
            'permissions_by_category': self.permissions_by_category(permissions),
        }, status=status.HTTP_200_OK)


class CurrentUserView(APIView):

    @staticmethod
    def permissions_by_category(permissions):
        categories = set({i.split('_')[-1] for i in permissions})
        categories = {i: [] for i in categories}
        for permission in permissions:
            category_part = permission.split('_')[-1]
            categories[category_part].append(permission)
        return categories

    def get(self, request, *args, **kwargs):
        user = request.user
        permissions = user.role.values_list('role_permissions__permission', flat=True)
        return Response({
            'user_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'middle_name': user.middle_name,
            'region': user.region_id,
            'district': user.district_id,
            'permissions': permissions,
            'permissions_by_category': self.permissions_by_category(permissions),
        })


class JWTObtainPairView(TokenObtainPairView):
    serializer_class = JWTObtainPairSerializer
    permission_classes = [AllowAny, ]
