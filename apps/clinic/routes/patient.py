from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from apps.clinic.models import Patient
from apps.clinic.serializers.patient import PatientDetailSerializer, PatientSerializer
from config.views import BaseModelViewSet


class PatientViewSet(BaseModelViewSet):
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PatientDetailSerializer
        return PatientSerializer

    def get_queryset(self):
        queryset = Patient.objects.select_related('region', 'district')

        region = self.request.query_params('region')
        gender = self.request.query_params('gender')
        search = self.request.query_params('search')

        if region:
            queryset = queryset.filter(region__id=region)
        if gender:
            queryset = queryset.filter(gender=gender)
        if search:
            queryset = queryset.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search))
        return queryset
