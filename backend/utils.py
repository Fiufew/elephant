import io
import os

from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import fitz

FONT_SIZE = 7
NUMBER_PDF_PAGE = 0


def car_image_upload_to(instance, filename):
    car_name = instance.car_name
    year = instance.year_manufactored
    return f"files_dir/cars/{car_name}_{year}/{filename}"


def other_files_path_for_application(instance, filename): # пока не работает
    """Функция создания пути к прочим файлам."""
    folder = os.path.join(
        settings.MEDIA_ROOT,
        "other_files", f"Application_{instance.application_id}")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, filename)


def create_text_layer_with_coordinates(
        font_name, font_size, text_data, output_path):
    """Создания текста по координатам."""
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)
    c.setFont(font_name, font_size)
    for text, (x, y) in text_data.items():
        c.drawString(x, y, text)
    c.save()
    packet.seek(0)
    with open(output_path, "wb") as f:
        f.write(packet.getvalue())


def merge_pdfs(template_path, text_layer_path, output_path):
    """Слияние pdf-файлов."""
    with fitz.open(template_path) as template_pdf:
        with fitz.open(text_layer_path) as text_layer_pdf:
            for page_num in range(template_pdf.page_count):
                page = template_pdf[page_num]
                page.show_pdf_page(page.rect, text_layer_pdf, NUMBER_PDF_PAGE)
            template_pdf.save(output_path)


def generate_pdf(
        application,
        folder_name,
        template_name,
        output_name,
        data_key,
        text_positions):
    """Генерация PDF файла."""
    application_folder = os.path.join(
        settings.MEDIA_ROOT,
        f"files_dir/applications/{folder_name}/Application_{application.id}")
    os.makedirs(application_folder, exist_ok=True)
    template_path = f"backend/pdf_create/{template_name}"
    output_path = os.path.join(
        application_folder, f"{output_name}_№{application.id}.pdf")
    temp_text_pdf = os.path.join(application_folder, "temp_text.pdf")
    pdfmetrics.registerFont(TTFont(
        "Calibri", "backend/pdf_create/font_Calibri.ttf"))
    create_text_layer_with_coordinates(
        "Calibri", FONT_SIZE, text_positions, temp_text_pdf)
    merge_pdfs(template_path, temp_text_pdf, output_path)
    setattr(
        application,
        data_key,
        f"files_dir/applications/{folder_name}/"
        f"Application_{application.id}/{output_name}_№{application.id}.pdf")
    application.save()
    os.remove(temp_text_pdf)
    return output_path


def pdf_create_contract(request, application):
    """Функция создания договора."""
    text_positions = {
        f"{application.renter_name}": (160, 648),  # имя
    }
    generate_pdf(
        application, "contracts",
        "contract_template.pdf", "Contract", "contract", text_positions)
    return HttpResponseRedirect(reverse(
        "backend:application_detail", args=[application.id]))


def pdf_create_vaucher(request, application):
    """Функция создания ваучера."""
    text_positions = {
        f"{application.renter_name}": (200, 700),  # имя
    }
    generate_pdf(
        application, "vauchers",
        "vaucher_template.pdf", "Vaucher", "vaucher", text_positions)
    return HttpResponseRedirect(reverse(
        "backend:application_detail", args=[application.id]))
