from rest_framework import serializers

from apps.location.models import Region, District


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name_uz']


class DistrictSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(read_only=True, source='region.name_uz')

    class Meta:
        model = District
        fields = ['id', 'name_uz', 'region_name']
