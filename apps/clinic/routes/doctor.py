from rest_framework.permissions import IsAuthenticated

from apps.clinic.models import Doctor
from apps.clinic.serializers.doctor import DoctorSerializer, DoctorDetailSerializer
from config.views import BaseModelViewSet


class DoctorViewSet(BaseModelViewSet):
    permission_classes = [IsAuthenticated, ]
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DoctorDetailSerializer
        return DoctorSerializer

    def get_queryset(self):
        queryset = Doctor.objects.select_related('specialization', 'user')

        specialization = self.request.query_params('specialization')
        is_active = self.request.query_params('is_active')
        if specialization:
            queryset = queryset.filter(specialization__id=specialization)
        if is_active:
            queryset = queryset.filter(is_active=is_active)
        return queryset


