import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.sessions.base_session import AbstractBaseSession
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from config import settings
from config.models import BaseModel


class AuthToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=1)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    @classmethod
    def create_token(cls, user, session_id):
        cls.objects.filter(sessions__id=session_id).delete()
        return cls.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(days=7)
        )

    def __str__(self):
        return f"Token {self.id}-(user: {self.user.username})"

    class Meta:
        db_table = 'access_tokens'


class Session(AbstractBaseSession):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # id = models.CharField(primary_key=True, default=generate_uuid, editable=False, db_index=True, max_length=36)
    expire_date = models.DateTimeField(_("expire date"), db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    session_key = None
    session_data = None
    access_token = models.ForeignKey(AuthToken, on_delete=models.SET_NULL, null=True, related_name='sessions')
    temp_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                  related_name='temp_user_sessions')
    is_deleted = models.BooleanField(default=False, db_default=False)
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_deleted',
        null=True
    )

    class Meta:
        db_table = 'sessions'

    @classmethod
    def get_session_store_class(cls):
        from django.contrib.sessions.backends.db import SessionStore
        return SessionStore


class SessionTempUser(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session_temp_user_logs')
    temp_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name='session_temp_user_logs')

    class Meta:
        db_table = 'session_temp_users'


class User(AbstractUser, BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    middle_name = models.CharField(_('middle name'), max_length=30, blank=True)
    settings = models.JSONField(null=True, blank=True)

    password = models.CharField(_("password"), max_length=128, null=True)

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(_("username"), max_length=150, null=True, blank=True, unique=True,
                                help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
                                validators=[username_validator],
                                error_messages={"unique": _("A user with that username already exists.")})

    role = models.ManyToManyField('Role', through='UserRole', through_fields=('user', 'role'), related_name='users')
    region = models.ForeignKey('location.Region', on_delete=models.SET_NULL, null=True, related_name='users')
    district = models.ForeignKey('location.District', on_delete=models.SET_NULL, null=True, related_name='users')

    class Meta:
        db_table = 'users'


class PermissionTypes(models.TextChoices):
    CREATE_USER = 'CREATE_USER', 'Foydalanuvchilarni yaratish'
    UPDATE_USER = 'UPDATE_USER', 'Foydalanuvchilarni o`zgartirish'
    VIEW_USER = 'VIEW_USER', 'Foydalanuvchilarni ko`rish'
    DELETE_USER = 'DELETE_USER', 'Foydalanuvchilarni o`chirish'

    CREATE_ROLE = 'CREATE_ROLE', 'Ro`llarni yaratish'
    UPDATE_ROLE = 'UPDATE_ROLE', 'Ro`llarni o`zgartirish'
    VIEW_ROLE = 'VIEW_ROLE', 'Ro`llarni ko`rish'
    DELETE_ROLE = 'DELETE_ROLE', 'Ro`llarni o`chirish'

    @staticmethod
    def category_name(category_code):
        category_names = {
            'USER': 'Foydalanuvchilar',
            'ROLE': 'Ro`llar'
        }
        return category_names[category_code]


class Role(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)

    class Meta:
        db_table = 'roles'


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.CharField(max_length=55, choices=PermissionTypes.choices)

    def __str__(self):
        return f'{self.permission}'

    class Meta:
        db_table = 'roles_permissions'


class UserRole(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='users_roles')
    role = models.ForeignKey('Role', on_delete=models.CASCADE, related_name='users_roles')

    class Meta:
        db_table = 'users_roles'
        # unique_together = ('user', 'role')


class AuthLog(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip = models.CharField(max_length=30, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='auth_logs'
    )

    is_active = models.BooleanField(default=True, db_default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_created',
        null=True,
        db_column='created_by'
    )
    modified_at = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_modified',
        null=True,
        db_column='modified_by'
    )
    is_deleted = models.BooleanField(default=False, db_default=False)
    deleted_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_deleted',
        null=True,
        db_column='deleted_by'
    )

    class Meta:
        db_table = 'auth_logs'
