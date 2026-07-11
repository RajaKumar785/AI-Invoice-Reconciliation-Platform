import streamlit as st
from pdf2image import convert_from_path
from PIL import Image
import tempfile
import os

POPPLER_PATH = r"D:\Download\Release-26.02.0-0\poppler-26.02.0\Library\bin"


def show_pdf_preview(po_file, invoice_file):

    st.markdown("---")
    st.subheader("📑 Document Preview")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🏢 Purchase Order")

        if po_file is not None:

            if po_file.name.lower().endswith(".pdf"):

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:

                    tmp.write(po_file.getbuffer())

                    pdf_path = tmp.name

                pages = convert_from_path(
                    pdf_path,
                    poppler_path=POPPLER_PATH
                )

                st.image(
                    pages[0],
                    use_container_width=True
                )

                os.remove(pdf_path)

            else:

                image = Image.open(po_file)

                st.image(
                    image,
                    use_container_width=True
                )

    with col2:

        st.markdown("### 🧾 Vendor Invoice")

        if invoice_file is not None:

            if invoice_file.name.lower().endswith(".pdf"):

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:

                    tmp.write(invoice_file.getbuffer())

                    pdf_path = tmp.name

                pages = convert_from_path(
                    pdf_path,
                    poppler_path=POPPLER_PATH
                )

                st.image(
                    pages[0],
                    use_container_width=True
                )

                os.remove(pdf_path)

            else:

                image = Image.open(invoice_file)

                st.image(
                    image,
                    use_container_width=True
                )