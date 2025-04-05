import io
import os

import fitz
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

FONT_SIZE = 7
NUMBER_PDF_PAGE = 0


def generate_contract(application):
    bid_folder = f"files/applications/Application_{application.num}/contracts/"
    os.makedirs(bid_folder, exist_ok=True)

    base_path = os.path.join(settings.BASE_DIR, "items/pdf_generator")
    template_path = os.path.join(base_path, "contract_template.pdf")
    font_path = os.path.join(base_path, "Calibri.ttf")

    output_path = os.path.join(bid_folder, f"Contract_№{application.num}.pdf")
    temp_text_pdf = os.path.join(bid_folder, "text_for_contracts.pdf")

    data = {"Name": application.client_name}

    pdfmetrics.registerFont(TTFont("Calibri", font_path))

    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)
    c.setFont("Calibri", FONT_SIZE)
    c.drawString(160, 648, f"{data['Name']}")
    c.save()
    packet.seek(0)

    with open(temp_text_pdf, "wb") as f:
        f.write(packet.getvalue())

    with fitz.open(template_path) as template_pdf:
        with fitz.open(temp_text_pdf) as text_layer_pdf:
            for page_num in range(template_pdf.page_count):
                page = template_pdf[page_num]
                page.show_pdf_page(page.rect, text_layer_pdf, NUMBER_PDF_PAGE)
            template_pdf.save(output_path)

    application.contract = f"files/applications/Application_{application.num}/contracts/Договор_№{application.id}.pdf"
    application.save()


def generate_vaucher(application):
    bid_folder = f"files/applications/Application_{application.num}/vauchers/"
    os.makedirs(bid_folder, exist_ok=True)

    base_path = os.path.join(settings.BASE_DIR, "items/pdf_generator")
    template_path = os.path.join(base_path, "vaucher_template.pdf")
    font_path = os.path.join(base_path, "Calibri.ttf")

    output_path = os.path.join(bid_folder, f"Vaucher_№{application.num}.pdf")
    temp_text_pdf = os.path.join(bid_folder, "text_for_vauchers.pdf")

    data = {"Name": application.client_name}

    pdfmetrics.registerFont(TTFont("Calibri", font_path))

    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)
    c.setFont("Calibri", FONT_SIZE)
    c.drawString(160, 648, f"{data['Name']}")
    c.save()
    packet.seek(0)

    with open(temp_text_pdf, "wb") as f:
        f.write(packet.getvalue())

    with fitz.open(template_path) as template_pdf:
        with fitz.open(temp_text_pdf) as text_layer_pdf:
            for page_num in range(template_pdf.page_count):
                page = template_pdf[page_num]
                page.show_pdf_page(page.rect, text_layer_pdf, NUMBER_PDF_PAGE)
            template_pdf.save(output_path)

    application.vaucher = f"files/applications/Application_{application.num}/vauchers/Vaucher_№{application.num}.pdf"
    application.save()

