from django.http import JsonResponse, HttpResponseBadRequest
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist

from .models import Car, Application, Files
from .forms import CarForm, PriceForm, ApplicationForm
from .utils import pdf_create_contract, pdf_create_vaucher
from .services import ApplicationService, PriceService, CarService


def index(request):
    '''
    Отображает список автомобилей на главной странице
    '''
    try:
        search_query = request.GET.get('search', '')
        booked_only = request.GET.get('booked_only', '').lower() == 'true'
        cars = CarService.get_filtered_cars(search_query, booked_only)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            cars_data = [
                {
                    'brand': car.brand.name,
                    'model': car.model.name,
                    'color': car.color.name,
                    'year_manufactored': car.year_manufactored,
                    'license_plate': car.license_plate,
                    'is_availaible': car.is_availaible,
                    'detail_url': reverse(
                        'backend:car_detail', args=[car.slug]),
                    'edit_url': reverse(
                        'backend:car_edit', args=[car.slug]),
                }
                for car in cars
            ]
            return JsonResponse({'cars': cars_data})

        return render(request, 'index.html', {'cars': cars})

    except ObjectDoesNotExist:
        return HttpResponseBadRequest("Объект не найден.")
    except Exception as e:
        return HttpResponseBadRequest(f"Произошла ошибка: {str(e)}")


def car_detail(request, slug):
    """
    Отображает детали автомобиля и информацию о занятых датах.

    Args:
        request (HttpRequest): Объект запроса.
        slug (str): Уникальный идентификатор автомобиля.

    Returns:
        HttpResponse: Отрендеренный HTML-шаблон с деталями автомобиля и
        информацией о занятых датах.
    """
    car = get_object_or_404(Car, slug=slug)

    context = {
        'car': car
    }
    return render(request, 'car_detail.html', context)


def create_car(request):
    """
    Отображает форму для создания нового автомобиля и
    обрабатывает отправку формы.

    Args:
        request (HttpRequest): Объект запроса.

    Returns:
        HttpResponse: Отрендеренный HTML-шаблон с формой или перенаправление на
                    страницу списка автомобилей.
    """
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('backend:car_list')
    else:
        form = CarForm()
    return render(request, 'car_form.html', {'form': form})


def edit_car(request, slug):
    """
    Отображает форму для редактирования
    автомобиля и обрабатывает отправку формы.

    Args:
        request (HttpRequest): Объект запроса.
        slug (str): Уникальный идентификатор автомобиля.

    Returns:
        HttpResponse: Отрендеренный HTML-шаблон с формой или перенаправление на
                    страницу с деталями автомобиля.
    """
    car = get_object_or_404(Car, slug=slug)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('backend:car_detail', slug=car.slug)
    else:
        form = CarForm(instance=car)
    return render(request, 'car_form.html', {'form': form, 'car': car})


def remove_car(request, slug):
    """
    Удаляет автомобиль и перенаправляет на страницу списка автомобилей.

    Args:
        request (HttpRequest): Объект запроса.
        slug (str): Уникальный идентификатор автомобиля.

    Returns:
        HttpResponse: Перенаправление на страницу списка автомобилей.
    """
    car = get_object_or_404(Car, slug=slug)
    if request.method == 'POST':
        car.delete()
        return redirect('backend:car_list')
    return redirect('backend:car_edit', slug=car.slug)


def applications_list(request):
    """
    Отображает список всех заявок.

    Args:
        request (HttpRequest): Объект запроса.

    Returns:
        HttpResponse: Отрендеренный HTML-шаблон со списком заявок или
        JSON-ответ для AJAX-запросов.
    """
    applications = Application.objects.select_related('car').values(
        'id',
        'status',
        'dropoff_time',
        'renter_name',
        'pickup_time',
        'dropoff_location',
        'pickup_location',
        'car__car_name',
    )
    return render(request, 'application_list.html', {
        'applications': applications
        })


def application_detail(request, pk):
    """
    Отображает детали конкретной заявки и позволяет добавлять/изменять файлы.
    """
    applications = get_object_or_404(
        Application.objects.select_related('car'), pk=pk)
    all_files = Files.objects.prefetch_related(
        'application').filter(application_id=applications.id)
    return render(
        request, 'application_detail.html',
        {
            'application': applications,
            'car': applications.car,
            'all_files': all_files
        })


def create_application(request):
    """
    Отображает форму для создания новой заявки и обрабатывает отправку формы.

    Args:
        request (HttpRequest): Объект запроса.

    Returns:
        HttpResponse: Отрендеренный HTML-шаблон с формой или перенаправление на
                    страницу списка заявок.
    """
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save()
            pdf_create_contract(request, application)
            pdf_create_vaucher(request, application)
            return redirect('backend:applications')
    else:
        form = ApplicationForm()
    return render(request, 'application_form.html', {'form': form})


def edit_application(request, pk):
    """
    Отображает форму для редактирования заявки и обрабатывает отправку формы.

    Args:
        request (HttpRequest): Объект запроса.
        pk (int): Первичный ключ заявки.

    Returns:
        HttpResponse: Отрендеренный HTML-шаблон с формой или перенаправление на
                    страницу с деталями заявки.
    """
    application = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(
            request.POST, request.FILES, instance=application
        )
        if form.is_valid():
            form.save()
            return redirect('backend:applications')
    else:
        form = ApplicationForm(instance=application)
    return render(request,
                  'application_form.html',
                  {'form': form, 'application': application})


def remove_application(request, pk):
    """
    Удаляет ставку и перенаправляет на страницу списка заявок.

    Args:
        request (HttpRequest): Объект запроса.
        pk (int): Первичный ключ ставки.

    Returns:
        HttpResponse: Перенаправление на страницу списка заявки.
    """
    application = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        application.delete()
        return redirect('backend:applications')
    return redirect('backend:applications')


def take_in_work_view(request, pk):
    username = request.user.username
    ApplicationService.take_in_work(pk, username)
    return redirect('backend:Application_list')


def create_price(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        form = PriceForm(request.POST)
        if form.is_valid():
            price_data = form.cleaned_data
            PriceService.create_price(car, price_data)
            return redirect('backend:car_list')
    else:
        form = PriceForm(initial={'car_price': car})
    return render(request, 'price_form.html', {
        'form': form,
        'car': car,
        'price_exists': False
        })


def update_price(request, pk):
    car = get_object_or_404(Car, pk=pk)
    price = car.price
    if request.method == 'POST':
        form = PriceForm(request.POST, instance=price)
        if form.is_valid():
            price_data = form.cleaned_data
            PriceService.update_price(price, price_data)
            return redirect('backend:car_list')
    else:
        form = PriceForm(instance=price)
    return render(request, 'price_form.html', {'form': form,
                                               'car': car,
                                               'price_exists': True})
