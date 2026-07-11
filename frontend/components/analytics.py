import streamlit as st
import pandas as pd


def show_analytics(history):

    st.markdown("---")
    st.header("📊 Analytics Dashboard")

    if not history:

        st.warning("No invoices processed yet.")
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

    total = len(df)

    approved = len(df[df["Status"] == "APPROVED"])

    hold = len(df[df["Status"] == "HOLD"])

    approval_rate = round((approved / total) * 100, 2)

    avg_score = round(df["Match Score"].astype(float).mean(), 2)

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Total", total)

    c2.metric("Approved", approved)

    c3.metric("Hold", hold)

    c4.metric("Approval %", f"{approval_rate}%")

    c5.metric("Avg Score", f"{avg_score}%")

    st.markdown("---")

    st.subheader("Invoice Status")

    chart = df["Status"].value_counts()

    st.bar_chart(chart)