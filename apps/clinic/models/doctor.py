import uuid

from django.conf import settings
from django.db import models

from apps.clinic.models import Specialization
from config.models import BaseModel


class SalaryType(models.TextChoices):
    PERCENTAGE = 'PERCENTAGE', 'foiz tizimi'
    FIXED = 'FIXED', 'fiksi tizimi'

class WorkDay(models.TextChoices):
    MONDAY = 'MONDAY', 'Dushanba'
    TUESDAY = 'TUESDAY', 'Seshanba'
    WEDNESDAY = 'WEDNESDAY', 'Chorshanba'
    THURSDAY = 'THURSDAY', 'Payshanba'
    FRIDAY = 'FRIDAY', 'Juma'
    SATURDAY = 'SATURDAY', 'Shanba'
    SUNDAY = 'SUNDAY', 'Yakshanba'

class Doctor(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='doctor_profile')
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctors')
    phone_number = models.CharField(max_length=20)
    work_start_time = models.TimeField()
    work_end_time = models.TimeField()
    work_days = models.JSONField(default=list)
    salary_type = models.CharField(max_length=20, choices=SalaryType.choices, default=SalaryType.PERCENTAGE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fixed_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    room_number = models.CharField(max_length=100, blank=True, null=True)
    experience_years = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'doctors'

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialization.name_uz}"
