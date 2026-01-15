from rest_framework.routers import DefaultRouter

from apps.clinic.routes.doctor import DoctorViewSet
from apps.clinic.routes.patient import PatientViewSet
from apps.clinic.routes.service import ServiceCategoryViewSet, ServiceViewSet
from apps.clinic.routes.specialization import SpecializationModelViewSet

router = DefaultRouter()
router.register('specializations', SpecializationModelViewSet, basename='specialization')
router.register('service-categories', ServiceCategoryViewSet, basename='service-category')
router.register('services', ServiceViewSet, basename='service')
router.register('doctors', DoctorViewSet, basename='doctor')
router.register('patients', PatientViewSet, basename='patient')

urlpatterns = router.urls
