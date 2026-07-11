import re


# --------------------------------------------------
# Detect Table Rows
# --------------------------------------------------

def is_table_row(line):

    line = line.strip()

    if len(line) < 10:
        return False

    # At least one number must exist
    if not re.search(r"\d", line):
        return False

    # Ignore headers
    ignore = [
        "description",
        "item description",
        "qty",
        "quantity",
        "rate",
        "unit",
        "amount",
        "subtotal",
        "grand total",
        "cgst",
        "sgst",
        "gst",
        "hsn"
    ]

    lower = line.lower()

    if any(word in lower for word in ignore):
        return False

    return True


# --------------------------------------------------
# Clean Table Line
# --------------------------------------------------

def clean_line(line):

    line = re.sub(r"\s{2,}", " ", line)

    line = line.replace("|", " ")

    line = line.strip()

    return line


# --------------------------------------------------
# Extract Table Rows
# --------------------------------------------------

def extract_table_lines(text):

    lines = text.split("\n")

    rows = []

    for line in lines:

        line = clean_line(line)

        if is_table_row(line):

            rows.append(line)

    return "\n".join(rows)