# Módulo para extracción de texto mediante OCR

import pytesseract
from PIL import Image
import pdfplumber

class OCRExtractor:
    def extract_from_image(self, image_path):
        """Extrae texto de una imagen (JPG, PNG, etc.)"""
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text

    def extract_from_pdf(self, pdf_path):
        """Extrae texto de un PDF, página por página"""
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

# Ejemplo de uso:
# ocr = OCRExtractor()
# texto = ocr.extract_from_image('cedula.jpg')
# texto_pdf = ocr.extract_from_pdf('certificacion.pdf')
