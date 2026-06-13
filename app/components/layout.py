import streamlit as st
from pathlib import Path

LOGO_PATH = Path("app/assets/logo.png")


def load_styles():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f8fbff 0%, #eef4ff 100%);
    }

    .main-card {
        background: white;
        padding: 2rem;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(30, 64, 175, 0.12);
        border: 1px solid #e5e7eb;
    }

    .title {
        font-size: 42px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0;
    }

    .subtitle {
        color: #64748b;
        font-size: 18px;
    }

    .bio-button {
        width: 100%;
        padding: 1.2rem;
        border-radius: 18px;
        border: 1px solid #dbeafe;
        background: white;
        text-align: center;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.08);
    }
    </style>
    """, unsafe_allow_html=True)


def show_logo(width=260):
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=width)
    else:
        st.markdown("### 🧬 BioLearn")


def top_bar():
    col1, col2 = st.columns([1, 4])
    with col1:
        show_logo(120)
    with col2:
        st.markdown("<p style='text-align:right;'>👤 Nombre usuario</p>", unsafe_allow_html=True)
