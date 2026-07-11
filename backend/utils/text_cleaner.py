import re


def clean_ocr_text(text):

    if not text:
        return ""

    # -----------------------------------
    # Normalize Line Endings
    # -----------------------------------

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # -----------------------------------
    # Remove Tabs
    # -----------------------------------

    text = text.replace("\t", " ")

    # -----------------------------------
    # Replace Common OCR Symbols
    # -----------------------------------

    replacements = {
        "|": " ",
        "¦": " ",
        "—": "-",
        "–": "-",
        "“": "\"",
        "”": "\"",
        "‘": "'",
        "’": "'"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # -----------------------------------
    # Remove Multiple Spaces
    # -----------------------------------

    text = re.sub(r"[ ]{2,}", " ", text)

    # -----------------------------------
    # Remove Multiple Blank Lines
    # -----------------------------------

    text = re.sub(r"\n{2,}", "\n", text)

    # -----------------------------------
    # Remove Trailing Spaces
    # -----------------------------------

    text = re.sub(r"[ \t]+\n", "\n", text)

    # -----------------------------------
    # Strip
    # -----------------------------------

    return text.strip()