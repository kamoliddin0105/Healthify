from rest_framework.permissions import IsAuthenticated

from apps.clinic.models import ServiceCategory, Service
from apps.clinic.serializers.service import ServiceCategoryDetailSerializer, ServiceCategorySerializer, \
    ServiceDetailSerializer, ServiceSerializer
from config.views import BaseModelViewSet


class ServiceCategoryViewSet(BaseModelViewSet):
    queryset = ServiceCategory.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ServiceCategoryDetailSerializer
        return ServiceCategorySerializer


class ServiceViewSet(BaseModelViewSet):
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ServiceDetailSerializer
        return ServiceSerializer

    def get_queryset(self):
        queryset = Service.objects.select_related('category')

        category = self.request.query_params('category')
        min_price = self.request.query_params('min_price')
        max_price = self.request.query_params('max_price')
        if category:
            queryset = queryset.filter(category__id=category)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset
