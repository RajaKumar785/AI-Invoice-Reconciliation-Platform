import re


# --------------------------------------------------
# Text Normalization
# --------------------------------------------------

def normalize_text(value):

    if value is None:
        return ""

    value = str(value).lower().strip()

    value = re.sub(r"\s+", " ", value)

    return value


# --------------------------------------------------
# Amount Normalization
# --------------------------------------------------

def normalize_amount(value):

    if value is None:
        return 0.0

    value = str(value)

    value = value.replace(",", "")
    value = value.replace("₹", "")
    value = value.replace("INR", "")
    value = value.replace("Rs.", "")
    value = value.replace("/-", "")

    value = re.sub(r"[^0-9.]", "", value)

    try:

        return float(value)

    except:

        return 0.0


# --------------------------------------------------
# Quantity Normalization
# --------------------------------------------------

def normalize_quantity(value):

    value = normalize_text(value)

    value = value.replace("kgs", "kg")
    value = value.replace("kg.", "kg")

    value = value.replace("pcs.", "pcs")
    value = value.replace("pieces", "pcs")

    value = value.replace("nos", "pcs")
    value = value.replace("numbers", "pcs")

    value = value.replace(" ", "")

    return value


# --------------------------------------------------
# GST Normalization
# --------------------------------------------------

def normalize_gst(value):

    value = normalize_text(value)

    if value == "":
        return 0

    numbers = re.findall(r"\d+", value)

    if not numbers:
        return 0

    if "cgst" in value and "sgst" in value:

        if len(numbers) >= 2:

            return int(numbers[0]) + int(numbers[1])

    return int(numbers[0])