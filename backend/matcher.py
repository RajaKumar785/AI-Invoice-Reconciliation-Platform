from difflib import SequenceMatcher

from utils.normalizer import (
    normalize_text,
    normalize_amount,
    normalize_quantity,
    normalize_gst
)


# --------------------------------------------------
# Text Similarity
# --------------------------------------------------

def similarity(a, b):

    return round(

        SequenceMatcher(

            None,

            str(a).lower().strip(),

            str(b).lower().strip()

        ).ratio() * 100,

        2

    )


# --------------------------------------------------
# Compare Line Items
# --------------------------------------------------

def compare_items(po_items, invoice_items):

    matched = 0

    mismatches = []

    total = max(len(po_items), len(invoice_items))

    if total == 0:

        return 100, []

    for i in range(total):

        if i >= len(po_items):

            mismatches.append({

                "Field": f"Item {i+1}",

                "Expected": "",

                "Received": invoice_items[i]

            })

            continue

        if i >= len(invoice_items):

            mismatches.append({

                "Field": f"Item {i+1}",

                "Expected": po_items[i],

                "Received": ""

            })

            continue

        po = po_items[i]

        inv = invoice_items[i]

        # ----------------------------------
        # Description
        # ----------------------------------

        desc_similarity = similarity(

            normalize_text(

                po.get("Description", po.get("Item", ""))

            ),

            normalize_text(

                inv.get("Description", inv.get("Item", ""))

            )

        )

        desc_match = desc_similarity >= 90

        # ----------------------------------
        # Quantity
        # ----------------------------------

        qty_match = (

            normalize_quantity(

                po.get("Quantity", "")

            )

            ==

            normalize_quantity(

                inv.get("Quantity", "")

            )

        )

        # ----------------------------------
        # Unit Price
        # ----------------------------------

        po_price = normalize_amount(

            po.get("Unit Price", "")

        )

        inv_price = normalize_amount(

            inv.get("Unit Price", "")

        )

        tolerance = max(

            1,

            po_price * 0.01

        )

        price_match = abs(

            po_price - inv_price

        ) <= tolerance

        # ----------------------------------
        # Final Item Decision
        # ----------------------------------

        if desc_match and qty_match and price_match:

            matched += 1

        else:

            mismatches.append({

                "Field": f"Item {i+1}",

                "Expected": po,

                "Received": inv

            })

    score = round(

        (matched / total) * 100,

        2

    )

    return score, mismatches
# --------------------------------------------------
# Main Matching Function
# --------------------------------------------------

def match_documents(po_data, invoice_data):

    comparison = {}

    mismatches = []

    matched_fields = 0

    total_fields = 5

    # ------------------------------------------
    # Vendor
    # ------------------------------------------

    vendor_similarity = similarity(

        normalize_text(
            po_data.get("Vendor", "")
        ),

        normalize_text(
            invoice_data.get("Vendor", "")
        )

    )

    vendor_match = vendor_similarity >= 90

    comparison["Vendor"] = {

        "expected": po_data.get("Vendor", ""),

        "received": invoice_data.get("Vendor", ""),

        "match": vendor_match,

        "confidence": vendor_similarity

    }

    if vendor_match:

        matched_fields += 1

    else:

        mismatches.append({

            "Field": "Vendor",

            "Expected": po_data.get("Vendor", ""),

            "Received": invoice_data.get("Vendor", "")

        })

    # ------------------------------------------
    # PO Number
    # ------------------------------------------

    po_match = (

        normalize_text(
            po_data.get("PO Number", "")
        )

        ==

        normalize_text(
            invoice_data.get("PO Number", "")
        )

    )

    comparison["PO Number"] = {

        "expected": po_data.get("PO Number", ""),

        "received": invoice_data.get("PO Number", ""),

        "match": po_match

    }

    if po_match:

        matched_fields += 1

    else:

        mismatches.append({

            "Field": "PO Number",

            "Expected": po_data.get("PO Number", ""),

            "Received": invoice_data.get("PO Number", "")

        })

    # ------------------------------------------
    # GST
    # ------------------------------------------

    po_gst = normalize_gst(

        po_data.get("GST", "")

    )

    invoice_gst = normalize_gst(

        invoice_data.get("GST", "")

    )

    gst_match = po_gst == invoice_gst

    comparison["GST"] = {

        "expected": po_gst,

        "received": invoice_gst,

        "match": gst_match

    }

    if gst_match:

        matched_fields += 1

    else:

        mismatches.append({

            "Field": "GST",

            "Expected": po_gst,

            "Received": invoice_gst

        })

    # ------------------------------------------
    # Amount
    # ------------------------------------------

    po_amount = normalize_amount(

        po_data.get("Amount", "")

    )

    invoice_amount = normalize_amount(

        invoice_data.get("Amount", "")

    )

    tolerance = max(

        5,

        po_amount * 0.01

    )

    amount_match = abs(

        po_amount - invoice_amount

    ) <= tolerance

    comparison["Amount"] = {

        "expected": po_amount,

        "received": invoice_amount,

        "match": amount_match

    }

    if amount_match:

        matched_fields += 1

    else:

        mismatches.append({

            "Field": "Amount",

            "Expected": po_amount,

            "Received": invoice_amount

        })

    # ------------------------------------------
    # Item Wise Matching
    # ------------------------------------------

    item_score, item_mismatch = compare_items(

        po_data.get("Items", []),

        invoice_data.get("Items", [])

    )

    item_match = item_score >= 90

    comparison["Items"] = {

        "score": item_score,

        "match": item_match

    }

    if item_match:

        matched_fields += 1

    else:

        mismatches.extend(item_mismatch)
    

    # ------------------------------------------
    # Final Score
    # ------------------------------------------

    score = round(
        (matched_fields / total_fields) * 100,
        2
    )

    # ------------------------------------------
    # Final Status
    # ------------------------------------------

    status = "APPROVED" if score >= 95 else "HOLD"

    # ------------------------------------------
    # Risk Level
    # ------------------------------------------

    if score >= 95:

        risk = "LOW"

    elif score >= 80:

        risk = "MEDIUM"

    else:

        risk = "HIGH"

    # ------------------------------------------
    # Recommendation
    # ------------------------------------------

    if status == "APPROVED":

        recommendation = (
            "Purchase Order and Vendor Invoice matched successfully. "
            "Payment can be approved."
        )

    else:

        recommendation = (
            "Mismatch detected. Manual finance review is recommended."
        )

    # ------------------------------------------
    # Final Comparison Summary
    # ------------------------------------------

    comparison["Summary"] = {

        "Overall Score": score,

        "Status": status,

        "Risk": risk

    }

    # ------------------------------------------
    # Return Result
    # ------------------------------------------

    return {

        "status": status,

        "score": score,

        "confidence": score,

        "risk": risk,

        "recommendation": recommendation,

        "comparison": comparison,

        "mismatches": mismatches

    }