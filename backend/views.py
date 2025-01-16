from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Car
from .forms import CarForm, PriceForm
from .services import ApplicationService, PriceService


def index(request):
    '''
    Отображает список автомобилей
    на главной странице
    '''
    cars = Car.objects.values('license_plate', 'is_availaible', 'car_name')
    print(cars)

    return render(request, 'index.html', {'cars': cars})


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
    car = ...

    context = {
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
    car = ...
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
    car = ...
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
    applications = ...

    return render(request, 'application_list.html', {'applications': applications})


def application_detail(request, pk):
    """
    Отображает детали конкретной заявки и позволяет добавлять/изменять файлы.
    """
    applications = ...
    if request.method == 'POST':
        form = ...(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.applications = applications
            file_instance.save()
            return redirect('backend:application_detail', pk=pk)
    else:
        form = ...
    all_files = ...
    return render(
        request, 'application_detail.html',
        {'applications': applications, 'form': form, 'all_files': all_files}
    )


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
        form = ...
        if form.is_valid():
            application = form.save()
            pdf_create_contract(request, application)  # noqa
            pdf_create_vaucher(request, application)  # noqa  
            return redirect('backend:application_list')
    else:
        form = ...
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
    application = ...
    if request.method == 'POST':
        form = ...
        if form.is_valid():
            form.save()
            return redirect('backend:application_detail', pk=application.id)
    else:
        form = ...
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
    application = ...
    if request.method == 'POST':
        application.delete()
        return redirect('backend:application')
    return redirect('backend:application', pk=application.id)


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
            return redirect('backend:price_list')
    else:
        form = PriceForm(initial={'car_price': car})
    return render(request, 'price_form.html', {'form': form,
                                               'car': car,
                                               'price_exists': False})


def update_price(request, pk):
    car = get_object_or_404(Car, pk=pk)
    price = car.price
    if request.method == 'POST':
        form = PriceForm(request.POST, instance=price)
        if form.is_valid():
            price_data = form.cleaned_data
            PriceService.update_price(price, price_data)
            return redirect('backend:price_list')
    else:
        form = PriceForm(instance=price)
    return render(request, 'price_form.html', {'form': form,
                                               'car': car,
                                               'price_exists': True})
