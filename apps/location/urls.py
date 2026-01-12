from django.urls import path

from apps.location.views import LocationRegionAPIView, LocationDistrictAPIView

app_name = 'location'
urlpatterns = [
    path('agro/region/', LocationRegionAPIView.as_view(), name='region'),
    path('agro/district/', LocationDistrictAPIView.as_view(), name='district'),
]
