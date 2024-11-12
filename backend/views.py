from datetime import datetime, timedelta
import calendar

from django.shortcuts import render, get_object_or_404, redirect

from .models import Car, Bid
from .forms import CarForm, BidForm


def index(request):
    '''
    Отображает список автомобилей
    на главной странице
    '''
    car = Car.objects.all()
    return render(request, 'index.html', {'cars': car})


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
    # Получаем объект автомобиля по уникальному идентификатору (slug)
    car = get_object_or_404(Car, slug=slug)

    # Получаем текущую дату
    today = datetime.today().date()

    # Вычисляем первый день текущего месяца
    first_day_of_month = today.replace(day=1)

    # Вычисляем последний день текущего месяца
    last_day_of_month = today.replace(day=calendar.monthrange(today.year,
                                                              today.month)[1])

    # Получаем все заявки для данного автомобиля,
    # которые начинаются до или в последний день месяца
    # и заканчиваются после или в первый день месяца
    bids = Bid.objects.filter(car=car, pickup_time__lte=last_day_of_month,
                              dropoff_time__gte=first_day_of_month)

    # Инициализируем список для хранения занятых дат и их идентификаторов
    busy_dates_with_ids = []

    # Заполняем список занятых дат и их идентификаторов
    for bid in bids:
        current_date = bid.pickup_time.date()
        while current_date <= bid.dropoff_time.date():
            busy_dates_with_ids.append((current_date, bid.id))
            current_date += timedelta(days=1)

    # Инициализируем список для хранения всех дат в текущем месяце
    date_range = []
    current_date = first_day_of_month

    # Заполняем список всех дат в текущем месяце
    while current_date <= last_day_of_month:
        date_range.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)

    # Создаем контекст для передачи в шаблон
    context = {
        'busy_dates_with_ids': [(date.strftime('%Y-%m-%d'), bid_id)
                                for date, bid_id in busy_dates_with_ids],
        'date_range': date_range,
        'car': car,
    }

    # Рендерим шаблон с контекстом
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


def bid_list(request):
    """
    Отображает список всех заявок.

    Args:
        request (HttpRequest): Объект запроса.

    Returns:
        HttpResponse: Отрендеренный HTML-шаблон со списком заявок.
    """
    bid = Bid.objects.all()
    return render(request, 'bid_list.html', {'bids': bid})


def bid_detail(request, pk):
    """
    Отображает детали конкретной заявки.

    Args:
        request (HttpRequest): Объект запроса.
        pk (int): Первичный ключ заявки.

    Returns:
        HttpResponse: Отрендеренный HTML-шаблон с деталями заявки.
    """
    bid = get_object_or_404(Bid, pk=pk)
    car = bid.car
    return render(request, 'bid_detail.html', {'bid': bid, 'car': car})


def create_bid(request):
    """
    Отображает форму для создания новой заявки и обрабатывает отправку формы.

    Args:
        request (HttpRequest): Объект запроса.

    Returns:
        HttpResponse: Отрендеренный HTML-шаблон с формой или перенаправление на
                      страницу списка заявок.
    """
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('backend:bid_list')
    else:
        form = BidForm()
    return render(request, 'bid_form.html', {'form': form})


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


def edit_bid(request, pk):
    """
    Отображает форму для редактирования заявки и обрабатывает отправку формы.

    Args:
        request (HttpRequest): Объект запроса.
        pk (int): Первичный ключ заявки.

    Returns:
        HttpResponse: Отрендеренный HTML-шаблон с формой или перенаправление на
                      страницу с деталями заявки.
    """
    bid = get_object_or_404(Bid, pk=pk)
    if request.method == 'POST':
        form = BidForm(request.POST, instance=bid)
        if form.is_valid():
            form.save()
            return redirect('backend:bid_detail', pk=bid.id)
    else:
        form = BidForm(instance=bid)
    return render(request, 'bid_form.html', {'form': form, 'bid': bid})


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


def remove_bid(request, pk):
    """
    Удаляет ставку и перенаправляет на страницу списка заявок.

    Args:
        request (HttpRequest): Объект запроса.
        pk (int): Первичный ключ ставки.

    Returns:
        HttpResponse: Перенаправление на страницу списка заявки.
    """
    bid = get_object_or_404(Bid, pk=pk)
    if request.method == 'POST':
        bid.delete()
        return redirect('backend:bid_list')
    return redirect('backend:bid_list', pk=bid.id)
