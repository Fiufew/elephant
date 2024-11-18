from datetime import datetime, timedelta
import calendar
import io
import os

import fitz
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from .models import Car, Bid, Files, Price
from .forms import CarForm, BidForm, BidFormAddFiles, PriceForm


@login_required
def index(request):
    '''
    Отображает список автомобилей
    на главной странице
    '''
    search_query = request.GET.get('search', '')
    booked_only = request.GET.get('booked_only') == 'true'
    cars = Car.objects.all()

    if search_query:
        cars = cars.filter(
            Q(brand__name__icontains=search_query) |
            Q(model__name__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(state_number__icontains=search_query)
        )

    if booked_only:
        cars = cars.filter(is_booked=True)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cars_data = [
            {
                'brand': car.brand.name,
                'model': car.model.name,
                'color': car.color.name,
                'state_number': car.state_number,
                'is_booked': car.is_booked,
                'detail_url': reverse('backend:car_detail', args=[car.slug]),
                'edit_url': reverse('backend:car_edit', args=[car.slug]),
            }
            for car in cars
        ]
        return JsonResponse({'cars': cars_data})

    return render(request, 'index.html', {'cars': cars})


@login_required
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
    today = datetime.today().date()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = today.replace(day=calendar.monthrange(
        today.year, today.month)[1])
    bids = Bid.objects.filter(
        car=car, pickup_time__lte=last_day_of_month,
        dropoff_time__gte=first_day_of_month)
    busy_dates_with_ids = []
    for bid in bids:
        current_date = bid.pickup_time.date()
        while current_date <= bid.dropoff_time.date():
            busy_dates_with_ids.append((current_date, bid.id))
            current_date += timedelta(days=1)
    date_range = []
    current_date = first_day_of_month
    while current_date <= last_day_of_month:
        date_range.append(current_date.strftime('%Y.%m.%d'))
        current_date += timedelta(days=1)
    context = {
        'busy_dates_with_ids': [(date.strftime('%Y.%m.%d'), bid_id)
                                for date, bid_id in busy_dates_with_ids],
        'date_range': date_range,
        'car': car,
    }

    # Рендерим шаблон с контекстом
    return render(request, 'car_detail.html', context)


@login_required
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


@login_required
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


@login_required
def price_list(request):
    cars = Car.objects.all()
    return render(request, 'price_list.html', {'cars': cars})

@login_required
def bid_detail(request, pk):
    """
    Отображает детали конкретной заявки и позволяет добавлять/изменять файлы.
    """
    bid = get_object_or_404(Bid, pk=pk)
    if request.method == 'POST':
        form = BidFormAddFiles(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.bid = bid
            file_instance.save()
            return redirect('backend:bid_detail', pk=pk)
    else:
        form = BidFormAddFiles()
    all_files = Files.objects.filter(bid_id=bid.id)
    car = bid.car
    return render(
        request, 'bid_detail.html',
        {'bid': bid, 'car': car, 'form': form, 'all_files': all_files}
    )


@login_required
def delete_file(request, file_id):
    file_instance = get_object_or_404(Files, id=file_id)
    bid_pk = file_instance.bid.id
    file_instance.delete()
    return redirect('backend:bid_detail', pk=bid_pk)


@login_required
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
        form = BidForm(request.POST, request.FILES)
        if form.is_valid():
            bid = form.save()
            pdf_create_contract(request, bid)
            pdf_create_vaucher(request, bid)
            return redirect('backend:bid_list')
    else:
        form = BidForm()
    return render(request, 'bid_form.html', {'form': form})


@login_required
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


@login_required
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
        form = BidForm(request.POST, request.FILES, instance=bid)
        if form.is_valid():
            form.save()
            return redirect('backend:bid_detail', pk=bid.id)
    else:
        form = BidForm(instance=bid)
    return render(request, 'bid_form.html', {'form': form, 'bid': bid})


@login_required
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


@login_required
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


def pdf_create_contract(request, bid):
    bid_folder = os.path.join(settings.MEDIA_ROOT,
                              f"contracts/Заявка_{bid.id}")
    os.makedirs(bid_folder, exist_ok=True)
    template_path = "backend/pdf_create/договор элефант бланк.pdf"
    output_path = os.path.join(bid_folder, f"Договор_№{bid.id}.pdf")
    temp_text_pdf = os.path.join(bid_folder, "текст для договора.pdf")

    data = {"Name": bid.renter_name}

    pdfmetrics.registerFont(TTFont(
        "Calibri", "backend/pdf_create/ofont.ru_Calibri.ttf"))

    def create_text_layer(temp_text_pdf, data):
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=A4)
        c.setFont("Calibri", 7)
        c.drawString(160, 648, f"{data['Name']}")
        c.save()
        packet.seek(0)
        with open(temp_text_pdf, "wb") as f:
            f.write(packet.getvalue())

    def merge_pdfs(template_path, temp_text_pdf, output_path):
        with fitz.open(template_path) as template_pdf:
            with fitz.open(temp_text_pdf) as text_layer_pdf:
                for page_num in range(template_pdf.page_count):
                    page = template_pdf[page_num]
                    page.show_pdf_page(page.rect, text_layer_pdf, 0)
                template_pdf.save(output_path)
    create_text_layer(temp_text_pdf, data)
    merge_pdfs(template_path, temp_text_pdf, output_path)
    bid.contract = f"contracts/Заявка_{bid.id}/Договор_№{bid.id}.pdf"
    bid.save()
    return HttpResponseRedirect(reverse("backend:bid_detail", args=[bid.id]))


def pdf_create_vaucher(request, bid):
    bid_folder = os.path.join(settings.MEDIA_ROOT, f"vauchers/Заявка_{bid.id}")
    os.makedirs(bid_folder, exist_ok=True)
    template_path = "backend/pdf_create/ваучер бланк.pdf"
    output_path = os.path.join(bid_folder, f"Ваучер_№{bid.id}.pdf")
    temp_text_pdf = os.path.join(bid_folder, "текст для ваучера.pdf")

    data = {"Name": bid.renter_name}

    pdfmetrics.registerFont(TTFont(
        "Calibri", "backend/pdf_create/ofont.ru_Calibri.ttf"))

    def create_text_layer(temp_text_pdf, data):
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=A4)
        c.setFont("Calibri", 7)
        c.drawString(160, 648, f"{data['Name']}")
        c.save()
        packet.seek(0)
        with open(temp_text_pdf, "wb") as f:
            f.write(packet.getvalue())

    def merge_pdfs(template_path, temp_text_pdf, output_path):
        with fitz.open(template_path) as template_pdf:
            with fitz.open(temp_text_pdf) as text_layer_pdf:
                for page_num in range(template_pdf.page_count):
                    page = template_pdf[page_num]
                    page.show_pdf_page(page.rect, text_layer_pdf, 0)
                template_pdf.save(output_path)
    create_text_layer(temp_text_pdf, data)
    merge_pdfs(template_path, temp_text_pdf, output_path)
    bid.vaucher = f"vauchers/Заявка_{bid.id}/Ваучер_№{bid.id}.pdf"
    bid.save()
    return HttpResponseRedirect(reverse("backend:bid_detail", args=[bid.id]))


@require_POST
def take_in_work(request, pk):
    try:
        bid = Bid.objects.get(id=pk)
        bid.bid_preparer = request.user.username
        bid.save()
    except Bid.DoesNotExist:
        pass
    return redirect('backend:bid_list')


@login_required
def create_price(request, pk):
    car = Car.objects.get(id=pk)
    if request.method == 'POST':
        form = PriceForm(request.POST)
        if form.is_valid():
            price = form.save(commit=False)
            price.car_price = car
            price.save()
            return redirect('backend:price_list')
    else:
        form = PriceForm(initial={'car_price': car})
    return render(request, 'price_form.html', {'form': form,
                                               'car': car,
                                               'price_exists': False})


@login_required
def update_price(request, pk):
    car = Car.objects.get(id=pk)
    price = car.price
    if request.method == 'POST':
        form = PriceForm(request.POST, instance=price)
        if form.is_valid():
            form.save()
            return redirect('backend:price_list')
    else:
        form = PriceForm(instance=price)
    return render(request, 'price_form.html', {'form': form,
                                               'car': car,
                                               'price_exists': True})
