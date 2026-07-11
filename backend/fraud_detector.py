def detect_fraud(invoice_json):

    alerts = []

    amount = invoice_json["Total Amount"]
    gst = invoice_json["GST Percentage"]

    if amount > 500000:
        alerts.append("High invoice amount detected")

    if gst > 28:
        alerts.append("Suspicious GST percentage")

    if not alerts:
        alerts.append("No fraud detected")

    return alerts