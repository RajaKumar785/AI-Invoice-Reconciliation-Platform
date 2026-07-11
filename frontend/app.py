import streamlit as st
import sys
import os
import json

# ----------------------------------------------------
# Backend Path
# ----------------------------------------------------

sys.path.append(os.path.abspath("backend"))

# ----------------------------------------------------
# Frontend Components
# ----------------------------------------------------

from styles.theme import load_theme
from components.header import show_header
from components.metrics import show_metrics
from components.upload_panel import upload_documents
from components.processing_pipeline import show_processing_pipeline
from components.comparison_table import show_comparison
from components.decision_panel import show_decision
from components.analytics import show_analytics
from components.audit_logs import show_audit_logs
from components.pdf_preview import show_pdf_preview

# ----------------------------------------------------
# Backend Modules
# ----------------------------------------------------

from ocr import extract_text
from extractor import extract_document_data
from matcher import match_documents
from resolution_generator import generate_resolution_note

from utils.json_validator import validate_json

from database.models import (
    create_tables,
    save_invoice,
    invoice_exists,
    get_invoice_history
)

# ----------------------------------------------------
# Streamlit Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="InvoiceAI Finance Copilot",
    page_icon="🤖",
    layout="wide"
)

# ----------------------------------------------------
# Initialize Database
# ----------------------------------------------------

create_tables()

# ----------------------------------------------------
# Load Theme
# ----------------------------------------------------

load_theme()

# ----------------------------------------------------
# Header
# ----------------------------------------------------

show_header()

# ----------------------------------------------------
# Dashboard Metrics
# ----------------------------------------------------

history = get_invoice_history()

show_metrics(history)

# ----------------------------------------------------
# Upload Section
# ----------------------------------------------------

po_file, invoice_file, analyze = upload_documents()

# ----------------------------------------------------
# PDF Preview
# ----------------------------------------------------

if po_file or invoice_file:

    show_pdf_preview(
        po_file,
        invoice_file
    )

# ----------------------------------------------------
# Start Processing
# ----------------------------------------------------

if analyze:

    if po_file is None:

        st.error("Please upload Company Purchase Order.")

        st.stop()

    if invoice_file is None:

        st.error("Please upload Vendor Invoice.")

        st.stop()

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    # ----------------------------------------
    # Save Purchase Order
    # ----------------------------------------

    po_path = os.path.join(
        "uploads",
        po_file.name
    )

    with open(po_path, "wb") as f:

        f.write(
            po_file.getbuffer()
        )

    # ----------------------------------------
    # Save Vendor Invoice
    # ----------------------------------------

    invoice_path = os.path.join(
        "uploads",
        invoice_file.name
    )

    with open(invoice_path, "wb") as f:

        f.write(
            invoice_file.getbuffer()
        )

    # ----------------------------------------
    # Processing Animation
    # ----------------------------------------

    show_processing_pipeline()

        # ----------------------------------------
    # OCR + AI Extraction
    # ----------------------------------------

    with st.spinner("🤖 AI is processing the documents..."):

        po_text = extract_text(po_path)

        invoice_text = extract_text(invoice_path)

        po_response = extract_document_data(
            po_text,
            "Purchase Order"
        )

        invoice_response = extract_document_data(
            invoice_text,
            "Vendor Invoice"
        )

    # ----------------------------------------
    # OCR Output
    # ----------------------------------------

    st.markdown("---")

    st.subheader("📄 OCR Extraction")

    with st.expander(
        "Purchase Order OCR",
        expanded=False
    ):

        st.text_area(
            "Purchase Order OCR",
            po_text,
            height=250
        )

    with st.expander(
        "Vendor Invoice OCR",
        expanded=False
    ):

        st.text_area(
            "Vendor Invoice OCR",
            invoice_text,
            height=250
        )

    # ----------------------------------------
    # AI Raw Response (Debug)
    # ----------------------------------------

    with st.expander(
        "🤖 AI Raw Response",
        expanded=False
    ):

        st.write("Purchase Order Response")

        st.code(po_response)

        st.write("Vendor Invoice Response")

        st.code(invoice_response)

    # ----------------------------------------
    # Convert AI Response to JSON
    # ----------------------------------------

    try:

        po_json = validate_json(

            json.loads(

                po_response
                .replace("```json", "")
                .replace("```", "")
                .strip()

            )

        )

        invoice_json = validate_json(

            json.loads(

                invoice_response
                .replace("```json", "")
                .replace("```", "")
                .strip()

            )

        )

    except Exception as e:

        st.error("❌ AI returned invalid JSON")

        st.exception(e)

        st.subheader("Purchase Order Response")

        st.code(po_response)

        st.subheader("Vendor Invoice Response")

        st.code(invoice_response)

        st.stop()

    # ----------------------------------------
    # Duplicate Invoice Check
    # ----------------------------------------

    if invoice_exists(

        invoice_json.get(
            "Invoice Number",
            ""
        )

    ):

        st.error(
            "🚨 Duplicate Invoice Detected"
        )

        st.stop()

    # ----------------------------------------
    # Extracted JSON
    # ----------------------------------------

    st.markdown("---")

    st.subheader("🤖 AI Extracted Information")

    col1, col2 = st.columns(2)

    with col1:

        st.json(po_json)

    with col2:

        st.json(invoice_json)


    # ----------------------------------------
    # Intelligent Matching
    # ----------------------------------------

    result = match_documents(
        po_json,
        invoice_json
    )

    # ----------------------------------------
    # Comparison Table
    # ----------------------------------------

    st.markdown("---")

    show_comparison(
        po_json,
        invoice_json,
        result
    )

    st.metric(
        "🎯 Overall Match Score",
        f"{result['score']}%"
    )

    # ----------------------------------------
    # Decision Panel
    # ----------------------------------------

    show_decision(result)

    # ----------------------------------------
    # AI Resolution
    # ----------------------------------------

    st.markdown("---")

    st.subheader("🧠 AI Finance Resolution")

    with st.spinner("Generating AI Recommendation..."):

        resolution = generate_resolution_note(
            po_json,
            invoice_json,
            result
        )

    st.info(resolution)

    # ----------------------------------------
    # Save to Database
    # ----------------------------------------

    try:

        save_invoice(
            po_json,
            invoice_json,
            result
        )

    except Exception as e:

        st.error("❌ Database Error")

        st.exception(e)

    # ----------------------------------------
    # Refresh Dashboard Data
    # ----------------------------------------

    history = get_invoice_history()

    # ----------------------------------------
    # Analytics
    # ----------------------------------------

    st.markdown("---")

    tab1, tab2 = st.tabs(
        [
            "📊 Analytics Dashboard",
            "📜 Audit Trail"
        ]
    )

    with tab1:

        show_analytics(history)

    with tab2:

        show_audit_logs(history)

    # ----------------------------------------
    # Footer
    # ----------------------------------------

    st.markdown("---")

    st.caption(
        "🚀 InvoiceAI Finance Copilot | AI-Powered Invoice Reconciliation Platform"
    )