import easyocr
import pytesseract
from PIL import Image

# Initialize EasyOCR
reader = easyocr.Reader(['en'])


def extract_text(image_path):

    text = ""

    try:
        # -------- EasyOCR (primary) --------
        results = reader.readtext(image_path)

        for r in results:
            text += r[1] + " "

        if text.strip() != "":
            return text

    except Exception as e:
        print("EasyOCR failed, switching to Tesseract")

    # -------- fallback: Tesseract --------
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text

    except Exception as e:
        return "OCR failed"