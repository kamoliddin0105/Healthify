from rest_framework.permissions import IsAuthenticated

from apps.clinic.models import Specialization
from apps.clinic.serializers.specialization import SpecializationSerializer
from config.views import BaseModelViewSet


class SpecializationModelViewSet(BaseModelViewSet):
    queryset = Specialization.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = SpecializationSerializer
    lookup_field = 'pk'
