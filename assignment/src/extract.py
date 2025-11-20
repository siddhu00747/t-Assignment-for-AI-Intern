# src/extract.py
import pdfplumber
import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import tempfile

def extract_raw_pages(pdf_path, use_ocr_if_empty=True):
    """
    Returns list of pages: [{"page":1, "text": "..."}...]
    Uses pdfplumber for text extraction; if page text empty and OCR allowed, runs OCR.
    """
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            if not text and use_ocr_if_empty:
                # fallback OCR for that page
                text = ocr_page(pdf_path, pageno=i-1)
            pages.append({"page": i, "text": text})
    return pages

def ocr_page(pdf_path, pageno):
    """
    Convert single page to image and OCR it with pytesseract.
    pageno is 0-indexed.
    """
    try:
        images = convert_from_path(pdf_path, first_page=pageno+1, last_page=pageno+1)
        if images:
            text = pytesseract.image_to_string(images[0])
            return text
    except Exception:
        return ""
    return ""
