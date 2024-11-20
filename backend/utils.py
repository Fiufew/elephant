import io
import os

import fitz
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


def other_files_path(instance, filename):
    folder = os.path.join(
        settings.MEDIA_ROOT, f"other_files/Заявка_{instance.bid_id}")
    os.makedirs(folder, exist_ok=True)
    edit_str = f'other_files/Заявка_{instance.bid_id}/'
    return f'{edit_str}{filename}'


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
