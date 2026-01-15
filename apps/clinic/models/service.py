import uuid

from django.db import models

from config.models import BaseModel


class Service(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name_uz = models.CharField(max_length=200)
    name_ru = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('ServiceCategory', on_delete=models.PROTECT,
                                 related_name='services')
    duration = models.IntegerField(help_text='Qancha vaqt davom etishi')

    class Meta:
        db_table = 'services'

    def __str__(self):
        return self.name_uz
