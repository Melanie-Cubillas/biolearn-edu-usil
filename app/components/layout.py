from pathlib import Path
import unicodedata

import streamlit as st


LOGO_PATH = Path(__file__).resolve().parents[1] / "assets" / "logo.png"

NAV_ITEMS = [
    {"label": "Inicio", "page": "dashboard", "terms": ["inicio", "dashboard", "panel"]},
    {"label": "Enfermedades", "page": "diseases", "terms": ["enfermedades", "genes", "casos clinicos"]},
    {"label": "Transcripción", "page": "transcription", "terms": ["transcripcion", "adn", "arn", "arnm"]},
    {"label": "Traducción", "page": "translation", "terms": ["traduccion", "proteinas", "aminoacidos", "codones"]},
    {"label": "Mutaciones", "page": "mutation_recognition", "terms": ["mutaciones", "blast", "alineamiento"]},
    {"label": "Quiz", "page": "quiz", "terms": ["quiz", "evaluacion", "preguntas"]},
    {"label": "Tutoriales", "page": "tutorials", "terms": ["tutoriales", "guias", "fasta", "ncbi"]},
]

SEARCH_TARGETS = NAV_ITEMS + [
    {
        "label": "Enfermedad de Huntington",
        "page": "disease_detail",
        "disease": "huntington",
        "terms": ["huntington", "htt", "cag", "neurodegenerativa"],
    },
    {
        "label": "Anemia falciforme",
        "page": "disease_detail",
        "disease": "anemia_falciforme",
        "terms": ["anemia falciforme", "hbb", "hemoglobina", "gag", "gtg"],
    },
    {
        "label": "Fibrosis quística",
        "page": "disease_detail",
        "disease": "fibrosis_quistica",
        "terms": ["fibrosis quistica", "cftr", "delta f508", "delecion"],
    },
]


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
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 10px !important;
        border: 1px solid #CBD5E1 !important;
        background: #FFFFFF !important;
        color: #0F172A !important;
        font-size: 14.5px !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
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
        border: 1px solid #CBD5E1 !important;
        background: #FFFFFF !important;
        color: #4F46E5 !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.06) !important;
    }
    .stButton > button[kind="secondary"]:hover,
    .stButton > button.stBaseButton-secondary:hover {
        border-color: #4F46E5 !important;
        background: rgba(99, 102, 241, 0.05) !important;
        color: #4F46E5 !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.12) !important;
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


def _normalize_search(value):
    normalized = unicodedata.normalize("NFKD", value or "")
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    return ascii_value.lower().strip()


def _find_search_matches(query, limit=4):
    normalized_query = _normalize_search(query)
    if not normalized_query:
        return []

    matches = []
    for target in SEARCH_TARGETS:
        searchable = " ".join([target["label"], *target.get("terms", [])])
        if normalized_query in _normalize_search(searchable):
            matches.append(target)

    return matches[:limit]


def _go_to_target(target):
    if target.get("disease"):
        st.session_state.selected_disease = target["disease"]
    st.session_state.page = target["page"]


def _handle_nav_search():
    matches = _find_search_matches(st.session_state.get("global_nav_search", ""), limit=1)
    if matches:
        _go_to_target(matches[0])


def top_bar():
    user = st.session_state.get("user", {})
    name = user.get("name", "Estudiante") if isinstance(user, dict) else "Estudiante"
    current_page = st.session_state.get("page", "dashboard")

    # Determinar destino de retroceso
    back_target = None
    if current_page == "diseases":
        back_target = "dashboard"
    elif current_page == "disease_detail":
        back_target = "diseases"
    elif current_page in ["transcription", "translation", "mutation_recognition"]:
        back_target = "disease_detail"
    elif current_page in ["quiz", "tutorials"]:
        back_target = "dashboard"

    st.markdown("""
    <style>
    /* Estilos del Header Premium */
    div[data-testid="stVerticalBlock"]:has(.custom-nav-trigger) {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(226, 232, 240, 0.9) !important;
        border-radius: 20px !important;
        padding: 0.8rem 1.6rem !important;
        margin-bottom: 2rem !important;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04) !important;
    }
    .nav-logo-text {
        font-size: 24px;
        font-weight: 800;
        background: linear-gradient(135deg, #1E3A8A 0%, #4F46E5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: flex;
        align-items: center;
        height: 40px;
        line-height: 40px;
        letter-spacing: -0.02em;
    }

    .nav-brand-subtitle {
        color: #93C5FD !important;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: .08em;
        text-transform: uppercase;
    }

    .nav-user-text {
        font-size: 14.5px;
        font-weight: 700;
        color: #475569 !important;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    with st.container():
        st.markdown('<div class="custom-nav-trigger"></div>', unsafe_allow_html=True)
        col_back, col_logo, col_nav_home, col_nav_learn, col_nav_quiz, col_nav_tut, col_user = st.columns([1, 1.8, 1, 2.2, 1, 1.1, 1.8])

        with col_back:
            if back_target:
                if st.button("← Atrás", key="nav_btn_back", use_container_width=True, type="secondary"):
                    st.session_state.page = back_target
                    st.rerun()
            else:
                st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

        with col_logo:
            st.markdown("<div class='nav-logo-text'>BioLearn</div>", unsafe_allow_html=True)

        with col_nav_home:
            is_active = current_page == "dashboard"
            if st.button("Inicio", key="nav_btn_home", use_container_width=True, type="primary" if is_active else "secondary"):
                st.session_state.page = "dashboard"
                st.rerun()

        with col_nav_learn:
            is_active = current_page in ["diseases", "disease_detail", "translation", "transcription", "mutation_recognition"]
            if st.button("Aprende Bioinformática", key="nav_btn_learn", use_container_width=True, type="primary" if is_active else "secondary"):
                st.session_state.page = "diseases"
                st.rerun()

        with col_nav_quiz:
            is_active = current_page == "quiz"
            if st.button("Quiz", key="nav_btn_quiz", use_container_width=True, type="primary" if is_active else "secondary"):
                st.session_state.page = "quiz"
                st.rerun()

        with col_nav_tut:
            is_active = current_page == "tutorials"
            if st.button("Tutoriales", key="nav_btn_tutorials", use_container_width=True, type="primary" if is_active else "secondary"):
                st.session_state.page = "tutorials"
                st.rerun()

        with col_user:
            st.markdown(f"<div class='nav-user-text'>{name}</div>", unsafe_allow_html=True)
