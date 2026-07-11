import streamlit as st


def show_metrics(history):

    total = len(history)

    approved = 0

    hold = 0

    average_score = 0

    if total > 0:

        approved = sum(
            1 for row in history
            if row[5] == "APPROVED"
        )

        hold = total - approved

        average_score = round(

            sum(float(row[6]) for row in history)

            / total,

            2

        )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📄 Total Documents",
        total
    )

    c2.metric(
        "✅ Approved",
        approved
    )

    c3.metric(
        "⏳ On Hold",
        hold
    )

    c4.metric(
        "🎯 Avg Match Score",
        f"{average_score}%"
    )