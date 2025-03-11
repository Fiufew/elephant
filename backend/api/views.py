from rest_framework import viewsets
from items.models import (
    Brand, CarModel, Problem, Engine, Music, Other,
    Insurance, Photo, Chassis, Car, Price, Date, Application, Misc
)
from .serializers import (
    BrandSerializer, CarModelSerializer, ProblemSerializer, EngineSerializer,
    MusicSerializer, OtherSerializer, InsuranceSerializer, PhotoSerializer,
    ChassisSerializer, CarSerializer, PriceSerializer, CarRentalDatesSerializer
)


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


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


class InsuranceViewSet(viewsets.ModelViewSet):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer


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
    serializer_class = CarRentalDatesSerializer


class MiscViewSet(viewsets.ModelViewSet):
    queryset = Misc.objects.all()
    serializer_class = CarRentalDatesSerializer
