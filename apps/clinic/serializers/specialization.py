from rest_framework import serializers

from apps.clinic.models import Specialization


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'name_uz', 'name_ru', 'description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


