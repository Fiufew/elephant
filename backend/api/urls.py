from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView,
)

from .views import (
    BrandViewSet, CarModelViewSet, ProblemViewSet,
    EngineViewSet, ChassisViewSet,
    ActViewSet, PhotoViewSet, FirstClassViewSet,
    CarViewSet, CarRentalDatesViewSet, SecondClassViewSet,
    ApplicationViewSet, MiscViewSet, TaxViewSet,
    MusicViewSet, OtherViewSet, UserRegistrationView
)

app_name = 'api'
router = routers.DefaultRouter()

router.register(
    r'brands', BrandViewSet, basename='brand'
)
router.register(
    r'models', CarModelViewSet, basename='car-model'
)
router.register(
    r'problems', ProblemViewSet, basename='problem'
)
router.register(
    r'engines', EngineViewSet, basename='engine'
)
router.register(
    r'music', MusicViewSet, basename='music'
)
router.register(
    r'others', OtherViewSet, basename='other'
)
router.register(
    r'act', ActViewSet, basename='act'
)
router.register(
    r'first-classes', FirstClassViewSet, basename='first-class'
)
router.register(
    r'second-classes', SecondClassViewSet, basename='second-class'
)
router.register(
    r'taxes', TaxViewSet, basename='tax'
)
router.register(
    r'photos', PhotoViewSet, basename='photo'
)
router.register(
    r'chassis', ChassisViewSet, basename='chassis'
)
router.register(
    r'cars', CarViewSet, basename='car'
)
router.register(
    r'rental-dates', CarRentalDatesViewSet, basename='rental-date'
)
router.register(
    r'applications', ApplicationViewSet, basename='application'
)
router.register(
    r'miscs', MiscViewSet, basename='misc'
)


urlpatterns = [
    path(
        '', include(router.urls)),
    path(
        'registration/', UserRegistrationView.as_view(), name='register'
    ),
    path(
        'token/', TokenObtainPairView.as_view(), name='token_obtain_pair'
    ),
    path(
        'token/refresh/', TokenRefreshView.as_view(), name='token_refresh'
    ),
    path(
        'token/verify/', TokenVerifyView.as_view(), name='token_verify'
    ),
]
