import streamlit as st


def load_styles():
    # Cargar Google Fonts via link tag (no @import dentro de style)
    st.markdown(
        '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">',
        unsafe_allow_html=True
    )

    st.markdown("""
    <style>
    /* Tipografía premium */
    html, body, .stApp, p, span, label, input, button, select, textarea {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

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

    /* Layout general */
    .block-container {
        max-width: 1200px !important;
        padding: 2rem 2rem 3rem 2rem !important;
    }

    /* Forzar fondo claro incluso en Dark Mode */
    .stApp {
        background: linear-gradient(135deg, #F8FAFC 0%, #EFF4FC 45%, #F5F0FF 100%) !important;
    }

    /* Forzar texto oscuro en elementos específicos */
    .stApp p, .stApp span, .stApp label, .stApp .auth-title, .stApp .auth-subtitle, .stApp .forgot-password-text, .stApp .hero-card-title, .stApp .hero-card-desc {
        color: #1E293B !important;
    }

    /* Tarjeta glassmorphic - SOLO el contenedor con borde del login */
    .login-card-wrapper {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(226, 232, 240, 0.8) !important;
        border-radius: 20px !important;
        padding: 2.5rem 2rem !important;
        box-shadow: 0 20px 45px rgba(15, 23, 42, 0.06) !important;
    }

    /* Títulos */
    .brand-logo {
        font-size: 30px;
        font-weight: 800;
        background: linear-gradient(135deg, #1E3A8A 0%, #4F46E5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        letter-spacing: -0.03em;
    }

    .auth-title {
        font-size: 32px;
        font-weight: 800;
        color: #0F172A !important;
        line-height: 1.25;
        margin-bottom: 0.75rem;
        letter-spacing: -0.02em;
    }

    .auth-subtitle {
        font-size: 15px;
        color: #64748B !important;
        line-height: 1.6;
        margin-bottom: 2rem;
    }

    .pill {
        display: inline-flex;
        align-items: center;
        background: #EFF6FF;
        color: #2563EB !important;
        padding: 0.4rem 1rem;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 1rem;
        border: 1px solid #DBEAFE;
    }

    /* Cajas informativas */
    .soft-box {
        background: linear-gradient(135deg, #E0F2FE, #EDE9FE);
        border-radius: 16px;
        padding: 1.25rem;
        margin: 1rem 0;
        color: #334155 !important;
        font-size: 15px;
    }

    /* Tarjetas del Hero */
    .hero-card {
        background: rgba(255, 255, 255, 0.75);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.25rem;
        display: flex;
        align-items: flex-start;
        gap: 1.25rem;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .hero-card:hover {
        transform: translateY(-2px);
        background: rgba(255, 255, 255, 0.95);
        border-color: rgba(99, 102, 241, 0.3);
        box-shadow: 0 12px 24px rgba(99, 102, 241, 0.08);
    }
    .hero-card-icon {
        font-size: 20px;
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
        color: #4F46E5;
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .hero-card-content {
        flex-grow: 1;
    }
    .hero-card-title {
        font-weight: 700;
        font-size: 15px;
        color: #1E293B !important;
        margin-bottom: 0.25rem;
    }
    .hero-card-desc {
        font-size: 13.5px;
        color: #64748B !important;
        line-height: 1.5;
    }

    /* ADN SVG */
    .dna-illustration-container {
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: flex-start;
    }
    .dna-helix-svg {
        width: 100%;
        max-width: 320px;
        height: auto;
    }

    /* Inputs */
    .stTextInput > div > div > input {
        border-radius: 10px !important;
        border: 1px solid #E2E8F0 !important;
        background: #FFFFFF !important;
        height: 40px !important;
        color: #0F172A !important;
        font-size: 14.5px !important;
        padding: 0 1rem !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #4F46E5 !important;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15) !important;
    }
    .stTextInput label {
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
    }

    /* Contraseña olvidada */
    .forgot-password-container {
        text-align: right;
        margin-top: -0.25rem;
        margin-bottom: 1.25rem;
    }
    .forgot-password-text {
        font-size: 13px;
        color: #94A3B8 !important;
        font-weight: 500;
    }

    /* Botones */
    .stButton > button {
        width: 100% !important;
        height: 40px !important;
        border-radius: 10px !important;
        font-size: 14.5px !important;
        cursor: pointer !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    /* Enlace de contraseña olvidada */
    div.st-key-forgot_password_btn button {
        border: none !important;
        background: transparent !important;
        color: #64748B !important;
        text-decoration: underline !important;
        font-size: 13.5px !important;
        height: auto !important;
        padding: 0 !important;
        box-shadow: none !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    div.st-key-forgot_password_btn button:hover {
        color: #4F46E5 !important;
        background: transparent !important;
        text-decoration: underline !important;
    }

    /* Botón Primario */
    .stButton > button[kind="primary"],
    .stButton > button.stBaseButton-primary {
        border: none !important;
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.25) !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button.stBaseButton-primary:hover {
        transform: translateY(-1.5px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.35) !important;
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%) !important;
        color: white !important;
    }

    /* Botón Secundario */
    .stButton > button[kind="secondary"],
    .stButton > button.stBaseButton-secondary {
        border: 1px solid #D8E2EF !important;
        background: #FFFFFF !important;
        color: #4F46E5 !important;
        font-weight: 600 !important;
    }
    .stButton > button[kind="secondary"]:hover,
    .stButton > button.stBaseButton-secondary:hover {
        border-color: #4F46E5 !important;
        background: rgba(99, 102, 241, 0.04) !important;
        color: #4F46E5 !important;
    }

    /* Responsividad */
    @media (max-width: 900px) {
        .block-container {
            padding: 2rem 1rem !important;
        }
        .auth-title {
            font-size: 26px;
        }
        .auth-subtitle {
            font-size: 14px;
            margin-bottom: 1.5rem;
        }
        .brand-logo {
            font-size: 26px;
            margin-bottom: 1.25rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def brand_logo():
    st.markdown(
        "<div class='brand-logo'>BioLearn</div>",
        unsafe_allow_html=True
    )


def top_bar():
    user = st.session_state.get("user", {})
    name = user.get("name", "Estudiante") if isinstance(user, dict) else "Estudiante"
    current_page = st.session_state.get("page", "dashboard")

    st.markdown("""
    <style>
    .nav-logo-text {
        font-size: 24px;
        font-weight: 800;
        color: #0F172A;
        display: flex;
        align-items: center;
        height: 40px;
        line-height: 40px;
    }
    .nav-user-text {
        font-size: 14.5px;
        font-weight: 600;
        color: #475569;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        height: 40px;
        line-height: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

    col_logo, col_nav1, col_nav2, col_nav3, col_user = st.columns([2.5, 1, 1, 1, 2.5])

    with col_logo:
        st.markdown("<div class='nav-logo-text'>BioLearn</div>", unsafe_allow_html=True)

    with col_nav1:
        is_active = current_page in ["dashboard", "diseases", "disease_detail", "translation", "transcription", "mutation_recognition"]
        if st.button("Inicio", key="nav_btn_home", use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state.page = "dashboard"
            st.rerun()

    with col_nav2:
        is_active = current_page == "quiz"
        if st.button("Quiz", key="nav_btn_quiz", use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state.page = "quiz"
            st.rerun()

    with col_nav3:
        is_active = current_page == "tutorials"
        if st.button("Tutoriales", key="nav_btn_tutorials", use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state.page = "tutorials"
            st.rerun()

    with col_user:
        st.markdown(f"<div class='nav-user-text'>{name}</div>", unsafe_allow_html=True)