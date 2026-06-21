import streamlit as st


def load_styles():
    st.markdown("""
    <style>
    [data-testid="stSidebar"],
    [data-testid="stSidebarNav"],
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
    }

    header {
        background: transparent !important;
    }

    [data-testid="stToolbar"] {
        display: flex !important;
        visibility: visible !important;
    }

    #MainMenu {
        display: block !important;
        visibility: visible !important;
    }

    footer {
        display: none !important;
        visibility: hidden !important;
    }

    .block-container {
        max-width: 1600px;
        padding: 2rem 2rem 3rem 2rem;
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
        border-radius: 16px !important;
        border: 1px solid #E2E8F0 !important;
        background: rgba(255,255,255,0.95) !important;
        height: 54px !important;
        color: #0F172A !important;
    }

    .stTextInput label {
        color: #334155 !important;
        font-weight: 700 !important;
    }

    .stButton > button {
        width: 100% !important;
        height: 58px !important;
        border: none !important;
        border-radius: 18px !important;
        background: linear-gradient(135deg, #60A5FA, #8B5CF6) !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        transition: all .25s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 10px 25px rgba(99,102,241,0.25);
        color: white !important;
    }

    @media (max-width: 900px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .auth-title {
            font-size: 38px;
        }

        .auth-subtitle {
            font-size: 16px;
        }

        .brand-logo {
            font-size: 28px;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def brand_logo():
    st.markdown(
        "<div class='brand-logo'>BioLearn 🧬</div>",
        unsafe_allow_html=True
    )


def top_bar():
    user = st.session_state.get("user", {})

    if isinstance(user, dict):
        name = user.get("name", "Estudiante")
    else:
        name = "Estudiante"

    st.html(f"""
    <div style="
        background:rgba(255,255,255,0.92);
        border-radius:28px;
        padding:1.4rem 2rem;
        display:flex;
        justify-content:space-between;
        align-items:center;
        box-shadow:0 14px 35px rgba(15,23,42,0.07);
        border:1px solid rgba(226,232,240,0.8);
        margin-bottom:2.8rem;
    ">
        <div style="
            font-size:32px;
            font-weight:900;
            color:#0F172A;
        ">
            BioLearn 🧬
        </div>

        <div style="
            display:flex;
            align-items:center;
            gap:.7rem;
            background:#FFFFFF;
            color:#0F172A;
            padding:.75rem 1.1rem;
            border-radius:999px;
            font-weight:900;
            font-size:16px;
        ">
            👤 {name}
            <span style="color:#64748B;"></span>
        </div>
    </div>
    """)