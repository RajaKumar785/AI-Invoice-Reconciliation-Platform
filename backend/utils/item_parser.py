import re


# --------------------------------------------------
# Check Item Row
# --------------------------------------------------

def is_item_row(line):

    line = line.strip()

    if len(line) < 10:
        return False

    # Must contain at least one decimal price
    if not re.search(r"\d+\.\d{2}", line):
        return False

    # Ignore totals
    ignore = [

        "subtotal",
        "grand total",
        "cgst",
        "sgst",
        "gst",
        "bank",
        "invoice",
        "vendor",
        "buyer"

    ]

    lower = line.lower()

    if any(word in lower for word in ignore):
        return False

    return True
# --------------------------------------------------
# Structure Item Lines
# --------------------------------------------------

def structure_items(text):

    lines = text.split("\n")

    output = []

    count = 1

    for line in lines:

        line = line.strip()

        if not is_item_row(line):
            continue

        line = re.sub(r"\s{2,}", " ", line)

        output.append(

            f"""
Item {count}

Raw Row:

{line}

------------------------
"""
        )

        count += 1

    return "\n".join(output)