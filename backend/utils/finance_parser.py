import re


# --------------------------------------------------
# Remove Duplicate Lines
# --------------------------------------------------

def remove_duplicate_lines(text):

    lines = text.split("\n")

    seen = set()

    cleaned = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line in seen:
            continue

        seen.add(line)

        cleaned.append(line)

    return "\n".join(cleaned)


# --------------------------------------------------
# Remove OCR Noise
# --------------------------------------------------

def remove_noise(text):

    replacements = {

        "Flardware": "Hardware",
        "ConGestie": "Angle",
        "ConGestiie": "Angle",
        "oo 40x40x5mm": "Angle 40x40x5mm",
        "GSTIN:": "GSTIN:",
        "Grand TotaI": "Grand Total",
        "GrandTotaI": "Grand Total"

    }

    for old, new in replacements.items():

        text = text.replace(old, new)

    return text


# --------------------------------------------------
# Normalize Spaces
# --------------------------------------------------

def normalize_spaces(text):

    text = re.sub(r"[ ]{2,}", " ", text)

    text = re.sub(r"\n{2,}", "\n", text)

    return text.strip()


# --------------------------------------------------
# Finance Parser
# --------------------------------------------------

def prepare_finance_text(text):

    text = remove_duplicate_lines(text)

    text = remove_noise(text)

    text = normalize_spaces(text)

    return text