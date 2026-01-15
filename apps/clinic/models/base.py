import uuid

from django.db import models

from config.models import BaseModel


class Specialization(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name_uz = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'specializations'

    def __str__(self):
        return self.name_uz


class ServiceCategory(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name_uz = models.CharField(max_length=200)
    name_ru = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    specialization = models.ForeignKey('Specialization', on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='service_categories')
    class Meta:
        db_table = 'service_categories'

    def __str__(self):
        return self.name_uz
