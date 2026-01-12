from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.authentication.models import (
    User, Role, RolePermission, UserRole,
    AuthToken, Session, AuthLog
)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'region', 'district', 'first_name', 'last_name', 'is_active', 'email','is_superuser')
    list_filter = ('username', 'region', 'district', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'middle_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Additional'), {'fields': ('settings',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission')
    list_filter = ('permission', 'role')
    search_fields = ('role__name',)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'role__name')
    ordering = ('-created_at',)


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'expires_at', 'is_expired')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('user__username',)
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'access_token', 'temp_user', 'expire_date', 'is_deleted')
    list_filter = ('is_deleted', 'created_at', 'expire_date')
    search_fields = ('temp_user__username',)
    ordering = ('-created_at',)


@admin.register(AuthLog)
class AuthLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username', 'ip')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'created_by', 'modified_at', 'modified_by')