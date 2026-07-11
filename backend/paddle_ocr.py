import os

from paddleocr import PaddleOCR

from pdf2image import convert_from_path

from utils.text_cleaner import clean_ocr_text


# -------------------------------------------------------
# Configuration
# -------------------------------------------------------

POPPLER_PATH = r"D:\Download\Release-26.02.0-0\poppler-26.02.0\Library\bin"


# -------------------------------------------------------
# Initialize PaddleOCR
# -------------------------------------------------------

ocr = PaddleOCR(
    lang="en"
)
# -------------------------------------------------------
# OCR From Image
# -------------------------------------------------------

def extract_text_from_image(image_path):

    result = ocr.predict(image_path)

    extracted_text = []

    try:

        for page in result:

            if hasattr(page, "res"):

                data = page.res

            elif isinstance(page, dict):

                data = page

            else:

                continue

            rec_texts = data.get("rec_texts", [])

            extracted_text.extend(rec_texts)

    except Exception as e:

        raise RuntimeError(
            f"PaddleOCR extraction failed: {e}"
        )

    text = "\n".join(extracted_text)

    return clean_ocr_text(text)


# -------------------------------------------------------
# OCR From PDF
# -------------------------------------------------------

def extract_text_from_pdf(file_path):

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    pages = convert_from_path(
        file_path,
        dpi=300,
        poppler_path=POPPLER_PATH
    )

    complete_text = ""

    for i, page in enumerate(pages):

        temp_path = os.path.join(
            "uploads",
            f"page_{i}.png"
        )

        page.save(
            temp_path,
            "PNG"
        )

        page_text = extract_text_from_image(
            temp_path
        )

        complete_text += page_text + "\n\n"

        if os.path.exists(temp_path):

            os.remove(temp_path)

    return clean_ocr_text(complete_text)
# -------------------------------------------------------
# Main OCR Function
# -------------------------------------------------------

def extract_text(file_path):

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension == ".pdf":

        return extract_text_from_pdf(
            file_path
        )

    elif extension in [

        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".tif",
        ".tiff"

    ]:

        return extract_text_from_image(
            file_path
        )

    else:

        raise ValueError(

            f"Unsupported file format: {extension}"

        ) 