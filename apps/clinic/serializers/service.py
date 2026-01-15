from rest_framework import serializers
from apps.clinic.models import ServiceCategory, Service


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name_uz', 'name_ru', 'description', 'specialization', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class ServiceCategoryDetailSerializer(ServiceCategorySerializer):
    services_count = serializers.SerializerMethodField()

    class Meta(ServiceCategorySerializer.Meta):
        fields = ServiceCategorySerializer.Meta.fields + ['services_count']

    def get_services_count(self, obj):
        return obj.services.count()


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name_uz', 'category', 'price', 'duration', 'is_active']
        read_only_fields = ['id', 'created_at']


class ServiceDetailSerializer(ServiceSerializer):
    category_detail = serializers.SerializerMethodField()

    class Meta(ServiceSerializer.Meta):
        fields = ServiceSerializer.Meta.fields + [
            'category_detail', 'name_ru', 'description', 'created_at'
        ]

    def get_category_detail(self, obj):
        if not obj.category:
            return None
        return ServiceCategorySerializer(obj.category).data