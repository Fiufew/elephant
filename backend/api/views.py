from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


from items.models import (
    CarBrand, CarModel, Problem, Engine, Chassis,
    Act, Photo, Car, FirstClass,
    Date, Application, Misc, Music,
    Other, SecondClass, Tax,
)
from .serializers import (
    CarBrandSerializer, CarModelSerializer, ProblemSerializer,
    ActSerializer, PhotoSerializer, ChassisSerializer,
    CarSerializer, CarRentalDatesSerializer,
    MusicSerializer, OtherSerializer, ApplicationSerializer,
    UserRegistrationSerializer, MiscSerializer, FirstClassSerializer,
    SecondClassSerializer, TaxSerializer, EngineSerializer,
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

    @action(detail=True, methods=['post'], url_path='solved')
    def mark_as_solved(self, request, pk=None):
        problem = self.get_object()
        problem.solve()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
