import re


def normalize_text(value):
    if value is None:
        return ""

    return str(value).lower().strip()


def normalize_amount(value):
    if value is None:
        return 0.0

    value = str(value)

    value = value.replace(",", "")
    value = value.replace("₹", "")
    value = value.strip()

    try:
        return float(value)
    except:
        return 0.0


def normalize_gst(gst):

    gst = normalize_text(gst)

    if not gst:
        return 0

    numbers = re.findall(r"\d+", gst)

    if len(numbers) >= 2 and "cgst" in gst and "sgst" in gst:
        return int(numbers[0]) + int(numbers[1])

    if len(numbers) >= 1:
        return int(numbers[0])

    return 0


def normalize_quantity(qty):

    qty = normalize_text(qty)

    qty = qty.replace("kgs", "kg")

    qty = qty.replace("pcs.", "pcs")

    qty = qty.replace(" ", "")

    return qty