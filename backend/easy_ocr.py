import easyocr
from easy_ocr import extract_text_easyocr

# ---------------------------------------
# Initialize Reader
# ---------------------------------------

reader = easyocr.Reader(
    ['en'],
    gpu=False
)


# ---------------------------------------
# Extract Text
# ---------------------------------------

def extract_text_from_image(image_path):

    processed = preprocess_image(image_path)

    # Temporary processed image
    temp_processed = "uploads/temp_processed.png"

    cv2.imwrite(
        temp_processed,
        processed
    )

    # -------------------------
    # EasyOCR
    # -------------------------

    easy_text = extract_text_easyocr(
        temp_processed
    )

    # -------------------------
    # Tesseract
    # -------------------------

    config = (
        "--oem 3 "
        "--psm 11 "
        "-c preserve_interword_spaces=1"
    )

    tess_text = pytesseract.image_to_string(
        processed,
        lang="eng",
        config=config
    )

    # Delete temp file
    if os.path.exists(temp_processed):
        os.remove(temp_processed)

    # -------------------------
    # Merge OCR Results
    # -------------------------

    final_text = easy_text + "\n\n" + tess_text

    return clean_ocr_text(final_text)