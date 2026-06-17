import streamlit as st


def load_styles():
    st.markdown("""
    <style>
    [data-testid="stSidebar"],
    [data-testid="stSidebarNav"],
    [data-testid="collapsedControl"],
    header,
    footer,
    #MainMenu {
        display: none !important;
        visibility: hidden !important;
    }

    .block-container {
        max-width: 1400px;
        padding: 2rem 3rem 4rem 3rem;
    }

    .stApp {
        background: linear-gradient(135deg, #F8FBFF 0%, #EEF4FF 45%, #F3EEFF 100%);
    }

    .brand-logo {
        font-size: 34px;
        font-weight: 900;
        color: #0F172A;
        margin-bottom: 1rem;
    }

    .auth-title {
        font-size: 52px;
        font-weight: 900;
        color: #1F2937;
        line-height: 1.05;
        margin-bottom: 1rem;
    }

    .auth-subtitle {
        font-size: 20px;
        color: #64748B;
        line-height: 1.6;
        margin-bottom: 2rem;
    }

    .pill {
        display: inline-block;
        background: #DBEAFE;
        color: #1D4ED8;
        padding: 0.6rem 1.1rem;
        border-radius: 999px;
        font-weight: 800;
        margin-bottom: 1.2rem;
    }

    .soft-box {
        background: linear-gradient(135deg, #E0F2FE, #EDE9FE);
        border-radius: 24px;
        padding: 1.3rem 1.5rem;
        margin: 1rem 0;
        color: #334155;
        font-size: 18px;
        line-height: 1.5;
    }

    .stTextInput > div > div > input {
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        background: rgba(255,255,255,0.85);
        height: 52px;
    }

    .stTextInput label {
        color: #334155 !important;
        font-weight: 700;
    }

    .stButton > button {
        width: 100%;
        height: 56px;
        border-radius: 18px;
        border: none;
        background: linear-gradient(135deg, #60A5FA, #8B5CF6);
        color: white;
        font-weight: 800;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(99,102,241,0.25);
        color: white;
    }

    @media (max-width: 900px) {
        .block-container {
            padding: 1.2rem;
        }

        .auth-title {
            font-size: 36px;
        }

        .auth-subtitle {
            font-size: 16px;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def brand_logo():
    st.markdown("<div class='brand-logo'>BioLearn 🧬</div>", unsafe_allow_html=True)


def top_bar():
    user = st.session_state.get("user", {})
    name = user.get("name", "Estudiante")

    st.markdown(f"""
    <div style="
        display:flex;
        justify-content:space-between;
        align-items:center;
        background:white;
        padding:1rem 1.5rem;
        border-radius:24px;
        box-shadow:0 8px 24px rgba(15,23,42,0.06);
        margin-bottom:2rem;
    ">
        <div style="font-size:24px;font-weight:900;color:#0F172A;">BioLearn 🧬</div>
        <div style="color:#475569;font-weight:700;">👤 {name}</div>
    </div>
    """, unsafe_allow_html=True)