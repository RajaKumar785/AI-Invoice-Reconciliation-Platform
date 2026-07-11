from backend.ocr import extract_text

text = extract_text("uploads/sample_invoice.pdf")

print(text)