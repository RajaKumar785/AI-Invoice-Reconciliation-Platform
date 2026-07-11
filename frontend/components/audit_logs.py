import streamlit as st
import pandas as pd


def show_audit_logs(history):

    st.markdown("---")
    st.header("📜 Audit Logs")

    if not history:

        st.warning("No audit history found.")
        return

    df = pd.DataFrame(
        history,
        columns=[
            "PO Number",
            "Invoice Number",
            "Vendor",
            "Amount",
            "GST",
            "Status",
            "Match Score",
            "Processed Time"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    csv = df.to_csv(index=False)

    st.download_button(

        "📥 Download Audit Report",

        csv,

        "audit_report.csv",

        "text/csv"

    )