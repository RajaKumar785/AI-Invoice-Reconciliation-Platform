import os
import cv2
import pytesseract
from pdf2image import convert_from_path

from utils.text_cleaner import clean_ocr_text

# -------------------------------------------------------
# Configuration
# -------------------------------------------------------

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

POPPLER_PATH = r"D:\Download\Release-26.02.0-0\poppler-26.02.0\Library\bin"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# -------------------------------------------------------
# Image Preprocessing
# -------------------------------------------------------

def preprocess_image(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(
            f"Unable to read image: {image_path}"
        )

    # Convert to Gray
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # Upscale for better OCR
    gray = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    # Noise Removal
    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    # Adaptive Threshold
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    # Morphological Closing
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (2, 2)
    )

    thresh = cv2.morphologyEx(
        thresh,
        cv2.MORPH_CLOSE,
        kernel
    )

    # Extra Noise Removal
    thresh = cv2.fastNlMeansDenoising(
        thresh,
        None,
        10,
        7,
        21
    )

    return thresh


# -------------------------------------------------------
# OCR From Image
# -------------------------------------------------------

def extract_text_from_image(image_path):

    processed = preprocess_image(image_path)

    config = (
        "--oem 3 "
        "--psm 11 "
        "-c preserve_interword_spaces=1 "
        "-c tessedit_char_whitelist="
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz"
        "0123456789"
        ".,:%()/+-₹ "
    )

    text = pytesseract.image_to_string(
        processed,
        lang="eng",
        config=config
    )

    return clean_ocr_text(text)


# -------------------------------------------------------
# OCR From PDF / Image
# -------------------------------------------------------

def extract_text(file_path):

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    extension = os.path.splitext(
        file_path
    )[1].lower()

    # ---------------------------------------------------
    # PDF OCR
    # ---------------------------------------------------

    if extension == ".pdf":

        pages = convert_from_path(
            file_path,
            poppler_path=POPPLER_PATH,
            dpi=400
        )

        complete_text = ""

        for i, page in enumerate(pages):

            temp_path = f"uploads/temp_page_{i}.png"

            page.save(
                temp_path,
                "PNG"
            )

            page_text = extract_text_from_image(
                temp_path
            )

            complete_text += page_text
            complete_text += "\n\n"

            if os.path.exists(temp_path):
                os.remove(temp_path)

        return clean_ocr_text(
            complete_text
        )

    # ---------------------------------------------------
    # Image OCR
    # ---------------------------------------------------

    return extract_text_from_image(
        file_path
    )