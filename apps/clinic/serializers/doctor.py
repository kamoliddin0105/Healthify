from rest_framework import serializers
from apps.clinic.models import Doctor
from apps.clinic.serializers.specialization import SpecializationSerializer


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialization', 'phone_number', 'room_number', 'is_active']


class DoctorDetailSerializer(DoctorSerializer):
    user_detail = serializers.SerializerMethodField()
    specialization_detail = serializers.SerializerMethodField()

    class Meta(DoctorSerializer.Meta):
        fields = DoctorSerializer.Meta.fields + [
            'user_detail', 'specialization_detail',
            'work_days', 'work_start_time', 'work_end_time', 'experience_years'
        ]

    def get_user_detail(self, obj):
        if not obj.user:
            return None
        return {
            'id': str(obj.user.id),
            'username': obj.user.username,
            'full_name': obj.user.get_full_name(),
        }

    def get_specialization_detail(self, obj):
        if not obj.specialization:
            return None
        return SpecializationSerializer(obj.specialization).data