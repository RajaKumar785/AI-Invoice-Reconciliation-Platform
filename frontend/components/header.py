import streamlit as st


def show_header():

    st.markdown(
        """
        <div class="main-title">
        🤖 InvoiceAI Finance Copilot
        </div>

        <div class="sub-title">
        AI Powered Purchase Order & Vendor Invoice Reconciliation Platform
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")