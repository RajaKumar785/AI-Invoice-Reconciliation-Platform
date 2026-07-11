import re


def extract_grand_total(text):

    patterns = [

        r"Grand\s*Total.*?([0-9,]+\.\d{2})",

        r"Grand\s*Total\s*\(INR\).*?([0-9,]+\.\d{2})",

        r"Total\s*Amount.*?([0-9,]+\.\d{2})",

        r"Net\s*Payable.*?([0-9,]+\.\d{2})"

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE | re.DOTALL
        )

        if match:

            return match.group(1)

    return ""