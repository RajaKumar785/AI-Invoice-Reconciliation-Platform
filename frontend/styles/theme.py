import streamlit as st

PRIMARY = "#2563EB"
SUCCESS = "#22C55E"
WARNING = "#F59E0B"
DANGER = "#EF4444"
BACKGROUND = "#0F172A"
CARD = "#1E293B"
TEXT = "#F8FAFC"


def load_theme():

    st.markdown(
        f"""
        <style>

        .stApp{{
            background:{BACKGROUND};
            color:{TEXT};
        }}

        section[data-testid="stSidebar"]{{
            background:#111827;
        }}

        h1,h2,h3,h4,h5{{
            color:white;
        }}

        .main-title{{
            font-size:42px;
            font-weight:700;
            color:white;
            margin-bottom:0px;
        }}

        .sub-title{{
            color:#CBD5E1;
            font-size:18px;
            margin-top:-8px;
        }}

        .card{{
            background:{CARD};
            padding:20px;
            border-radius:15px;
            border:1px solid #334155;
            box-shadow:0 0 15px rgba(0,0,0,.25);
        }}

        .metric-value{{
            font-size:34px;
            font-weight:bold;
            color:white;
        }}

        .metric-title{{
            color:#94A3B8;
            font-size:15px;
        }}

        .approved{{
            background:#052e16;
            border-left:6px solid {SUCCESS};
            padding:18px;
            border-radius:12px;
        }}

        .hold{{
            background:#450a0a;
            border-left:6px solid {DANGER};
            padding:18px;
            border-radius:12px;
        }}

        .upload-card{{
            background:{CARD};
            border:2px dashed {PRIMARY};
            border-radius:15px;
            padding:25px;
            text-align:center;
        }}

        .pipeline-card{{
            background:#111827;
            padding:15px;
            border-radius:10px;
            margin-bottom:12px;
        }}

        footer{{
            visibility:hidden;
        }}

        #MainMenu{{
            visibility:hidden;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )