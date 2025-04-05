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
    """
    Представление для управления марками автомобилей.

    Атрибуты:
        queryset: Все марки автомобилей.
        serializer_class: Сериализатор для марки автомобиля.
    """
    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer


class CarModelViewSet(viewsets.ModelViewSet):
    """
    Представление для управления моделями автомобилей.

    Атрибуты:
        queryset: Все модели автомобилей.
        serializer_class: Сериализатор для модели автомобиля.
    """
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer


class ProblemViewSet(viewsets.ModelViewSet):
    """
    Представление для управления проблемами автомобилей.

    Атрибуты:
        queryset: Все проблемы автомобилей.
        serializer_class: Сериализатор для проблемы автомобиля.

    Методы:
        mark_as_solved: Маркирует проблему как решенную.
    """
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    @action(detail=True, methods=['post'], url_path='solved')
    def mark_as_solved(self, request, pk=None):
        """
        Помечает проблему как решенную.

        Используется метод solve модели Problem для изменения статуса.
        """
        problem = self.get_object()
        problem.solve()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EngineViewSet(viewsets.ModelViewSet):
    """
    Представление для управления двигателями автомобилей.

    Атрибуты:
        queryset: Все двигатели автомобилей.
        serializer_class: Сериализатор для двигателя автомобиля.
    """
    queryset = Engine.objects.all()
    serializer_class = EngineSerializer


class MusicViewSet(viewsets.ModelViewSet):
    """
    Представление для управления музыкальными системами автомобилей.

    Атрибуты:
        queryset: Все музыкальные системы автомобилей.
        serializer_class: Сериализатор для музыкальной системы автомобиля.
    """
    queryset = Music.objects.all()
    serializer_class = MusicSerializer


class OtherViewSet(viewsets.ModelViewSet):
    """
    Представление для управления дополнительными особенностями автомобилей.

    Атрибуты:
        queryset: Все дополнительные особенности автомобилей.
        serializer_class: Сериализатор для дополнительных особенностей авто.
    """
    queryset = Other.objects.all()
    serializer_class = OtherSerializer


class ActViewSet(viewsets.ModelViewSet):
    """
    Представление для управления актами автомобилей.

    Атрибуты:
        queryset: Все акты автомобилей.
        serializer_class: Сериализатор для акта автомобиля.
    """
    queryset = Act.objects.all()
    serializer_class = ActSerializer


class FirstClassViewSet(viewsets.ModelViewSet):
    """
    Представление для управления первым классом автомобиля.

    Атрибуты:
        queryset: Все данные о первом классе автомобилей.
        serializer_class: Сериализатор для первого класса автомобиля.
    """
    queryset = FirstClass.objects.all()
    serializer_class = FirstClassSerializer


class SecondClassViewSet(viewsets.ModelViewSet):
    """
    Представление для управления вторым классом автомобиля.

    Атрибуты:
        queryset: Все данные о втором классе автомобилей.
        serializer_class: Сериализатор для второго класса автомобиля.
    """
    queryset = SecondClass.objects.all()
    serializer_class = SecondClassSerializer


class TaxViewSet(viewsets.ModelViewSet):
    """
    Представление для управления налогами автомобилей.

    Атрибуты:
        queryset: Все налоги автомобилей.
        serializer_class: Сериализатор для налога автомобиля.
    """
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    """
    Представление для управления фотографиями автомобилей.

    Атрибуты:
        queryset: Все фотографии автомобилей.
        serializer_class: Сериализатор для фотографии автомобиля.
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class ChassisViewSet(viewsets.ModelViewSet):
    """
    Представление для управления шасси автомобилей.

    Атрибуты:
        queryset: Все шасси автомобилей.
        serializer_class: Сериализатор для шасси автомобиля.
    """
    queryset = Chassis.objects.all()
    serializer_class = ChassisSerializer


class CarViewSet(viewsets.ModelViewSet):
    """
    Представление для управления автомобилями.

    Атрибуты:
        queryset: Все автомобили.
        serializer_class: Сериализатор для автомобиля.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarRentalDatesViewSet(viewsets.ModelViewSet):
    """
    Представление для управления датами аренды автомобилей.

    Атрибуты:
        queryset: Все даты аренды автомобилей.
        serializer_class: Сериализатор для дат аренды автомобилей.
    """
    queryset = Date.objects.all()
    serializer_class = CarRentalDatesSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    Представление для управления заявками на аренду автомобилей.

    Атрибуты:
        queryset: Все заявки на аренду автомобилей.
        serializer_class: Сериализатор для заявки на аренду.
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class MiscViewSet(viewsets.ModelViewSet):
    """
    Представление для управления прочими данными автомобилей.

    Атрибуты:
        queryset: Все прочие данные автомобилей.
        serializer_class: Сериализатор для прочих данных автомобиля.
    """
    queryset = Misc.objects.all()
    serializer_class = MiscSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    Представление для регистрации пользователя.

    Атрибуты:
        serializer_class: Сериализатор для регистрации пользователя.
        permission_classes: Разрешения для публичного доступа.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
