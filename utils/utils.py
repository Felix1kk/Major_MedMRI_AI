# utils/utils.py
import io
from PIL import Image
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import streamlit as st

def create_pdf(report_texts, images):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(name='Title', fontSize=24, leading=28, spaceAfter=12, alignment=1)
    normal_style = ParagraphStyle(name='Normal', fontSize=14, leading=18, spaceAfter=12)

    elements.append(Paragraph("MRI Analysis Report", title_style))
    elements.append(Spacer(1, 24))

    for i, (report_text, image_data) in enumerate(zip(report_texts, images)):
        elements.append(Paragraph(f"Image {i + 1}", normal_style))
        image = Image.open(io.BytesIO(image_data['data']))

        # Save image to a temporary file for ReportLab to use
        # Using a context manager for robust file handling
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            image_path = temp_file.name
            image.save(image_path)

        elements.append(RLImage(image_path, width=4 * inch, height=4 * inch))
        elements.append(Spacer(1, 12))

        # Handle bullet formatting
        for point in report_text.split('\n'):
            if point.strip().startswith("- "):
                elements.append(Paragraph(f"• {point.strip()[2:]}", normal_style))
            else:
                elements.append(Paragraph(point, normal_style))

        elements.append(Spacer(1, 24))
        if i < len(report_texts) - 1:
            elements.append(PageBreak())

    doc.build(elements)
    buffer.seek(0)
    return buffer

def create_translated_pdf(translated_text, target_language="English"):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(name='TranslatedTitle', fontSize=20, leading=24, spaceAfter=12, alignment=1)
    normal_style = ParagraphStyle(name='TranslatedNormal', fontSize=14, leading=18, spaceAfter=12)

    elements.append(Paragraph(f"Translated MRI Report ({target_language})", title_style))
    elements.append(Spacer(1, 24))

    # Split the translated text by newlines and add as paragraphs
    # This ensures proper wrapping and spacing in the PDF
    for line in translated_text.split('\n'):
        # Clean up common markdown like "###" or "**" if present from translation
        cleaned_line = line.replace("###", "").replace("**", "").strip()
        if cleaned_line: # Only add non-empty lines
            elements.append(Paragraph(cleaned_line, normal_style))
            # Add a small spacer between lines, adjust as needed for readability
            if not cleaned_line.endswith('.') and not cleaned_line.endswith('!') and not cleaned_line.endswith('?'):
                 elements.append(Spacer(1, 6)) # Add a small spacer if not ending in punctuation

    doc.build(elements)
    buffer.seek(0)
    return buffer

