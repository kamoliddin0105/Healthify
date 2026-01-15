import uuid

from django.db import models

from config.models import BaseModel


class Gender(models.TextChoices):
    MALE = 'MALE', 'Erkak'
    FEMALE = 'FEMALE', 'Ayol'


class Patient(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=Gender.choices)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    region = models.ForeignKey('location.Region', on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey('location.District', on_delete=models.SET_NULL, null=True, blank=True)
    allergies = models.TextField(blank=True, null=True)
    chronic_diseases = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'patients'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

