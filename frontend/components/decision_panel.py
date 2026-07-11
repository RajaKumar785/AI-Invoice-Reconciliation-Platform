import streamlit as st


def show_decision(result):

    st.markdown("---")
    st.subheader("⚖️ AI Finance Decision")

    status = result.get("status", "HOLD")
    score = result.get("score", 0)
    confidence = result.get("confidence", 0)
    risk = result.get("risk", "UNKNOWN")
    recommendation = result.get(
        "recommendation",
        "Manual review required."
    )

    # ---------------------------------------
    # Metrics
    # ---------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🎯 Match Score",
            f"{score}%"
        )

    with col2:

        st.metric(
            "🤖 Confidence",
            f"{confidence}%"
        )

    with col3:

        st.metric(
            "⚠️ Risk",
            risk
        )

    st.markdown("---")

    # ---------------------------------------
    # Final Decision
    # ---------------------------------------

    if status == "APPROVED":

        st.success("✅ PAYMENT APPROVED")

    else:

        st.error("❌ PAYMENT ON HOLD")

    # ---------------------------------------
    # Recommendation
    # ---------------------------------------

    st.info(
        f"💡 Recommendation:\n\n{recommendation}"
    )

    # ---------------------------------------
    # Mismatch Details
    # ---------------------------------------

    mismatches = result.get("mismatches", [])

    if len(mismatches) == 0:

        st.success("🎉 No mismatches found.")

        return

    st.subheader("📋 Mismatch Details")

    for item in mismatches:

        with st.expander(item["Field"]):

            st.write("**Expected**")

            st.code(str(item["Expected"]))

            st.write("**Received**")

            st.code(str(item["Received"]))