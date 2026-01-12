from django.db import connection
from rest_framework.views import APIView

from apps.location.models import Region, District
from apps.location.serializers import RegionSerializer, DistrictSerializer


class LocationRegionAPIView(APIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    def get_queryset(self):
        sql_raw = f"""SELECT id, name_uz FROM regions"""
        with connection.cursor() as cursor:
            cursor.execute(sql_raw)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results


class LocationDistrictAPIView(APIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    def get_queryset(self):
        region_id = self.kwargs['region_id']
        sql_raw = f"""SELECT id, name_uz FROM districts WHERE region_id = '{region_id}'"""
        with connection.cursor() as cursor:
            cursor.execute(sql_raw)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results
