from rest_framework import serializers
from apps.clinic.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'birth_date', 'gender']


class PatientDetailSerializer(PatientSerializer):
    age = serializers.SerializerMethodField()

    class Meta(PatientSerializer.Meta):
        fields = PatientSerializer.Meta.fields + [
            'middle_name', 'address', 'region', 'district',
            'allergies', 'chronic_diseases', 'created_at', 'age'
        ]

    def get_age(self, obj):
        from datetime import date
        today = date.today()
        return today.year - obj.birth_date.year - (
                (today.month, today.day) < (obj.birth_date.month, obj.birth_date.day)
        )