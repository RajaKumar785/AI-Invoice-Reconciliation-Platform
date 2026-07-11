import streamlit as st
import pandas as pd


def show_comparison(po_data, invoice_data, result):

    st.markdown("---")
    st.subheader("📊 Purchase Order vs Vendor Invoice")

    rows = []

    comparison = result["comparison"]

    matched = 0

    total = 0

    for field, value in comparison.items():

        if field == "Summary":
            continue

        total += 1

        status = "✅" if value["match"] else "❌"

        if value["match"]:
            matched += 1

        rows.append({

            "Field": field,

            "Purchase Order": value.get("expected", ""),

            "Vendor Invoice": value.get("received", ""),

            "Confidence": value.get("confidence", "-"),

            "Status": status

        })

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        return result["score"]