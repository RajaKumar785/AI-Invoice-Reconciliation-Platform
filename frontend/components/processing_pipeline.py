import streamlit as st
import time


def show_processing_pipeline():

    st.markdown("---")

    st.subheader("🤖 AI Processing Pipeline")

    progress = st.progress(0)

    steps = [

        "📄 Reading Purchase Order...",

        "📄 Reading Vendor Invoice...",

        "🔍 Running OCR...",

        "🤖 AI Extracting Data...",

        "⚖ Comparing Documents...",

        "📊 Calculating Match Score...",

        "✅ Finalizing Decision..."

    ]

    status = st.empty()

    for i, step in enumerate(steps):

        status.info(step)

        progress.progress((i + 1) / len(steps))

        time.sleep(0.4)

    status.success("Processing Completed ✅")