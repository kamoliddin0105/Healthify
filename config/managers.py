from django.db import models


class OnlyActivesManager(models.Manager):
    """
        Base Manager
        for show only active notes
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
