from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Brand, Price, Bid
from .forms import CarForm, BidForm


def index(request):
    car = Car.objects.all()
    return render(request, 'index.html', {'cars': car})


def car_detail(request, slug):
    car = get_object_or_404(Car, slug=slug)
    return render(request, 'car_detail.html', {'car': car})


def create_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('backend:car_list')
    else:
        form = CarForm()
    return render(request, 'car_form.html', {'form': form})  # не сохраняются фото


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
