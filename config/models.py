from django.db import models

from config import settings
from config.managers import OnlyActivesManager


class BaseModel(models.Model):
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

    # managers
    objects = OnlyActivesManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True