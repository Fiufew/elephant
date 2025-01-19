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


FONT_SIZE = 7
NUMBER_PDF_PAGE = 0


def other_files_path(instance, filename):
    folder = os.path.join(
        settings.MEDIA_ROOT, f"other_files/Application_{instance.application_id}")
    os.makedirs(folder, exist_ok=True)
    edit_str = f'other_files/Application_{instance.application_id}/'
    return f'{edit_str}{filename}'


def pdf_create_contract(request, application):
    application_folder = os.path.join(
        settings.MEDIA_ROOT, f"contracts/Application_{application.id}")
    os.makedirs(application_folder, exist_ok=True)
    template_path = "backend/pdf_create/contract_template.pdf"
    output_path = os.path.join(application_folder, f"Contract_№{application.id}.pdf")
    temp_text_pdf = os.path.join(application_folder, "текст для договора.pdf")

    data = {"Name": application.renter_name}

    pdfmetrics.registerFont(TTFont(
        "Calibri", "backend/pdf_create/font_Calibri.ttf"))

    def create_text_layer(temp_text_pdf, data):
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=A4)
        c.setFont("Calibri", FONT_SIZE)
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
                    page.show_pdf_page(
                        page.rect, text_layer_pdf, NUMBER_PDF_PAGE)
                template_pdf.save(output_path)
    create_text_layer(temp_text_pdf, data)
    merge_pdfs(template_path, temp_text_pdf, output_path)
    application.contract = f"contracts/Application_{application.id}/Contract_№{application.id}.pdf"
    application.save()
    return HttpResponseRedirect(reverse("backend:application_detail", args=[application.id]))


def pdf_create_vaucher(request, application):
    application_folder = os.path.join(
        settings.MEDIA_ROOT, f"vauchers/Application_{application.id}")
    os.makedirs(application_folder, exist_ok=True)
    template_path = "backend/pdf_create/vaucher_template.pdf"
    output_path = os.path.join(application_folder, f"Vaucher_№{application.id}.pdf")
    temp_text_pdf = os.path.join(application_folder, "текст для Vaucherа.pdf")

    data = {"Name": application.renter_name}

    pdfmetrics.registerFont(TTFont(
        "Calibri", "backend/pdf_create/font_Calibri.ttf"))

    def create_text_layer(temp_text_pdf, data):
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=A4)
        c.setFont("Calibri", FONT_SIZE)
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
                    page.show_pdf_page(
                        page.rect, text_layer_pdf, NUMBER_PDF_PAGE)
                template_pdf.save(output_path)
    create_text_layer(temp_text_pdf, data)
    merge_pdfs(template_path, temp_text_pdf, output_path)
    application.vaucher = f"vauchers/Application_{application.id}/Vaucher_№{application.id}.pdf"
    application.save()
    return HttpResponseRedirect(
        reverse("backend:application_detail", args=[application.id]))