from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Brand, Price, Bid
from .forms import CarForm, BidForm
from datetime import datetime, timedelta
import calendar


def index(request):
    car = Car.objects.all()
    return render(request, 'index.html', {'cars': car})


def car_detail(request, slug):
    car = get_object_or_404(Car, slug=slug)
    today = datetime.today().date()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = today.replace(day=calendar.monthrange(today.year,
                                                              today.month)[1])
    bids = Bid.objects.filter(car=car, pickup_time__lte=last_day_of_month,
                              dropoff_time__gte=first_day_of_month)
    busy_dates = []
    for bid in bids:
        current_date = bid.pickup_time.date()
        while current_date <= bid.dropoff_time.date():
            busy_dates.append(current_date)
            current_date += timedelta(days=1)
    date_range = []
    current_date = first_day_of_month
    while current_date <= last_day_of_month:
        date_range.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    context = {
        'busy_dates': [date.strftime('%Y-%m-%d') for date in busy_dates],
        'date_range': date_range,
        'car': car,
    }
    return render(request, 'car_detail.html', context)


def create_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('backend:car_list')
    else:
        form = CarForm()
    return render(request, 'car_form.html', {'form': form})


def bid_list(request):
    bid = Bid.objects.all()
    return render(request, 'bid_list.html', {'bids': bid})


def bid_detail(request, pk):
    bid = get_object_or_404(Bid, pk=pk)
    car = bid.car
    return render(request, 'bid_detail.html', {'bid': bid, 'car': car})


def create_bid(request):
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('backend:bid_list')
    else:
        form = BidForm()
    return render(request, 'bid_form.html', {'form': form})


def edit_car(request, slug):
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
    car = get_object_or_404(Car, slug=slug)
    if request.method == 'POST':
        car.delete()
        return redirect('backend:car_list')
    return redirect('backend:car_edit', slug=car.slug)


def remove_bid(request, pk):
    bid = get_object_or_404(Bid, pk=pk)
    if request.method == 'POST':
        bid.delete()
        return redirect('backend:bid_list')
    return redirect('backend:bid_list', pk=bid.id)


def calendar_view(request):
    # Получите текущую дату и дату через месяц
    today = datetime.today().date()
    next_month = today + timedelta(days=30)

    # Получите все аренды в этом диапазоне
    bids = Bid.objects.filter(pickup_time__lte=next_month, dropoff_time__gte=today)

    # Создайте список занятых дат
    busy_dates = []
    for bid in bids:
        current_date = bid.pickup_time.date()
        while current_date <= bid.dropoff_time.date():
            busy_dates.append(current_date)
            current_date += timedelta(days=1)

    # Создайте диапазон дат для календаря
    date_range = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]

    context = {
        'busy_dates': [date.strftime('%Y-%m-%d') for date in busy_dates],
        'date_range': date_range,
    }

    return render(request, 'calendar.html', context)
