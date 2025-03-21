from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    BrandViewSet, CarModelViewSet, ProblemViewSet,
    EngineViewSet, PriceViewSet, ChassisViewSet,
    InsuranceViewSet, PhotoViewSet,
    CarViewSet, CarRentalDatesViewSet,
    ApplicationViewSet, MiscViewSet,
    MusicViewSet, OtherViewSet
)

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'car-models', CarModelViewSet, basename='car-model')
router.register(r'problems', ProblemViewSet, basename='problem')
router.register(r'engines', EngineViewSet, basename='engine')
router.register(r'music', MusicViewSet, basename='music')
router.register(r'prices', PriceViewSet, basename='price')
router.register(r'others', OtherViewSet, basename='other')
router.register(r'insurances', InsuranceViewSet, basename='insurance')
router.register(r'photos', PhotoViewSet, basename='photo')
router.register(r'chassis', ChassisViewSet, basename='chassis')
router.register(r'cars', CarViewSet, basename='car')
router.register(
    r'rental-dates', CarRentalDatesViewSet, basename='rental-date')
router.register(
    r'applications', ApplicationViewSet, basename='application')
router.register(r'misc', MiscViewSet, basename='misc')


urlpatterns = [
    path('', include(router.urls)),
    path(
        'api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        'api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
        'api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
