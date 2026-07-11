REQUIRED_FIELDS = [
    "Vendor",
    "PO Number",
    "Invoice Number",
    "Document Date",
    "Items",
    "GST",
    "Amount"
]


def validate_json(data):

    # -----------------------------
    # Ensure dictionary
    # -----------------------------

    if not isinstance(data, dict):
        return {
            field: "" for field in REQUIRED_FIELDS
        } | {"Items": []}

    # -----------------------------
    # Add missing fields
    # -----------------------------

    for field in REQUIRED_FIELDS:

        if field not in data:

            if field == "Items":

                data[field] = []

            else:

                data[field] = ""

    # -----------------------------
    # Validate Items
    # -----------------------------

    if not isinstance(data["Items"], list):

        data["Items"] = []

    cleaned_items = []

    for item in data["Items"]:

        if not isinstance(item, dict):

            continue

        cleaned_items.append({

            "Description": item.get(
                "Description",
                item.get("Item", "")
            ),

            "Quantity": item.get(
                "Quantity",
                ""
            ),

            "Unit Price": item.get(
                "Unit Price",
                ""
            )

        })

    data["Items"] = cleaned_items

    # -----------------------------
    # Convert None → ""
    # -----------------------------

    for key in data:

        if data[key] is None:

            if key == "Items":

                data[key] = []

            else:

                data[key] = ""

    return data