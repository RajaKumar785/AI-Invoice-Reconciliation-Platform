import streamlit as st


def upload_documents():

    st.markdown("## 📂 Financial Document Upload")

    st.markdown(
        """
Upload the company Purchase Order and the Vendor Invoice.
The system will compare both documents using OCR + AI + Business Rules.
"""
    )

    left, right = st.columns(2)

    with left:

        st.markdown(
            """
<div class="card">

### 🏢 Company Purchase Order

Reference document issued by the company.

</div>
""",
            unsafe_allow_html=True,
        )

        purchase_order = st.file_uploader(
            "Upload Purchase Order",
            type=["pdf", "png", "jpg", "jpeg"],
            key="purchase_order",
        )

        if purchase_order is not None:

            st.success("Purchase Order Uploaded")

            st.write("**File Name:**", purchase_order.name)

            st.write(
                "**Size:**",
                round(purchase_order.size / 1024, 2),
                "KB",
            )

    with right:

        st.markdown(
            """
<div class="card">

### 🧾 Vendor Invoice

Invoice received from supplier.

</div>
""",
            unsafe_allow_html=True,
        )

        vendor_invoice = st.file_uploader(
            "Upload Vendor Invoice",
            type=["pdf", "png", "jpg", "jpeg"],
            key="vendor_invoice",
        )

        if vendor_invoice is not None:

            st.success("Vendor Invoice Uploaded")

            st.write("**File Name:**", vendor_invoice.name)

            st.write(
                "**Size:**",
                round(vendor_invoice.size / 1024, 2),
                "KB",
            )

    st.markdown("<br>", unsafe_allow_html=True)

    analyze = st.button(
        "🚀 Analyze Documents",
        type="primary",
        use_container_width=True,
    )

    return purchase_order, vendor_invoice, analyze