from rest_framework import viewsets, permissions, generics
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status

from items.models import (
    CarBrand, CarModel, Problem, Engine, Chassis,
    Act, Photo, Car, Price, FirstClass,
    Date, Application, Misc, Music,
    Other, SecondClass, Tax
)
from .serializers import (
    CarBrandSerializer, CarModelSerializer, ProblemSerializer, EngineSerializer,
    ActSerializer, PhotoSerializer, ChassisSerializer,
    CarSerializer, PriceSerializer, CarRentalDatesSerializer,
    MusicSerializer, OtherSerializer, ApplicationSerializer,
    UserRegistrationSerializer, MiscSerializer, FirstClassSerializer,
    SecondClassSerializer, TaxSerializer
)


class BrandViewSet(viewsets.ModelViewSet):
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer


class CarModelViewSet(viewsets.ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class EngineViewSet(viewsets.ModelViewSet):
    queryset = Engine.objects.all()
    serializer_class = EngineSerializer


class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer


class OtherViewSet(viewsets.ModelViewSet):
    queryset = Other.objects.all()
    serializer_class = OtherSerializer


class ActViewSet(viewsets.ModelViewSet):
    queryset = Act.objects.all()
    serializer_class = ActSerializer


class FirstClassViewSet(viewsets.ModelViewSet):
    queryset = FirstClass.objects.all()
    serializer_class = FirstClassSerializer


class SecondClassViewSet(viewsets.ModelViewSet):
    queryset = SecondClass.objects.all()
    serializer_class = SecondClassSerializer


class TaxViewSet(viewsets.ModelViewSet):
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class ChassisViewSet(viewsets.ModelViewSet):
    queryset = Chassis.objects.all()
    serializer_class = ChassisSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer


class CarRentalDatesViewSet(viewsets.ModelViewSet):
    queryset = Date.objects.all()
    serializer_class = CarRentalDatesSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class MiscViewSet(viewsets.ModelViewSet):
    queryset = Misc.objects.all()
    serializer_class = MiscSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
