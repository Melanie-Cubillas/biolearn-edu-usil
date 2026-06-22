import streamlit as st

from components.layout import load_styles, top_bar


DISEASES = [
    {
        "name": "Enfermedad de Huntington",
        "key": "huntington",
        "gene": "HTT",
        "description": "Trastorno genético asociado a repeticiones CAG en el gen HTT.",
        "bg_color": "#E0F2FE",
        "border_color": "#BAE6FD",
        "tag_color": "#1D4ED8",
        "tag_bg": "#FFFFFF",
    },
    {
        "name": "Anemia falciforme",
        "key": "anemia_falciforme",
        "gene": "HBB",
        "description": "Enfermedad hereditaria que altera la hemoglobina y la forma de los glóbulos rojos.",
        "bg_color": "#ffe8fa",
        "border_color": "#FBCFE8",
        "tag_color": "#DB2777",
        "tag_bg": "#FFFFFF",
    },
    {
        "name": "Fibrosis quística",
        "key": "fibrosis_quistica",
        "gene": "CFTR",
        "description": "Enfermedad genética relacionada con mutaciones en el gen CFTR.",
        "bg_color": "#DCFCE7",
        "border_color": "#BBF7D0",
        "tag_color": "#16A34A",
        "tag_bg": "#FFFFFF",
    },
]


def render_styles():
    st.markdown(
        """
        <style>
        .disease-title {
            font-size: 48px;
            font-weight: 900;
            color: #0F172A;
            margin-top: 2rem;
            margin-bottom: 0.8rem;
        }

        .disease-subtitle {
            font-size: 20px;
            color: #475569;
            margin-bottom: 2.5rem;
        }

        .disease-card {
            min-height: 390px;
            border-radius: 28px;
            padding: 2rem;
            box-shadow: 0 16px 34px rgba(15,23,42,0.07);
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }

        .disease-icon {
            width: 72px;
            height: 72px;
            border-radius: 22px;
            background: rgba(255,255,255,0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 34px;
            margin-bottom: 1.7rem;
            box-shadow: 0 10px 22px rgba(15,23,42,0.06);
        }

        .disease-name {
            font-size: 30px;
            line-height: 1.18;
            color: #0F172A;
            margin: 0 0 1rem 0;
            font-weight: 900;
        }

        .gene-badge {
            width: fit-content;
            display: inline-block;
            padding: .45rem .9rem;
            border-radius: 999px;
            font-size: 14px;
            font-weight: 900;
            margin-bottom: 1.5rem;
        }

        .disease-description {
            color: #475569;
            font-size: 17px;
            line-height: 1.55;
            margin: 0;
        }

        .stButton > button {
            border-radius: 16px !important;
            background: linear-gradient(135deg, #60A5FA, #8B5CF6) !important;
            color: white !important;
            border: none !important;
            height: 56px !important;
            font-weight: 800 !important;
            font-size: 16px !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 24px rgba(99,102,241,0.25);
        }

        @media (max-width: 900px) {
            .disease-title {
                font-size: 36px;
            }

            .disease-card {
                min-height: 340px;
                margin-bottom: 1rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def disease_card(disease):
    st.markdown(
        f"""
        <div class="disease-card" style="background:{disease['bg_color']}; border:1px solid {disease['border_color']};">
            <div style="font-size: 11px; font-weight: 800; color: {disease['tag_color']}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1rem;">Caso de Estudio</div>
            <div class="disease-name" style="margin-top: 0.5rem;">{disease['name']}</div>
            <div class="gene-badge" style="background:{disease['tag_bg']}; color:{disease['tag_color']};">
                Gen asociado: {disease['gene']}
            </div>
            <div class="disease-description">{disease['description']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Aprender", key=f"learn_{disease['key']}", use_container_width=True):
        st.session_state.selected_disease = disease["key"]
        new_progress = max(st.session_state.get("progress", 0), 20)
        st.session_state.progress = new_progress
        user = st.session_state.get("user", {})
        if isinstance(user, dict) and "email" in user:
            from services.progress_service import save_user_progress
            save_user_progress(
                user["email"],
                new_progress,
                st.session_state.get("streak", 1),
                st.session_state.get("badges", 0)
            )
        st.session_state.page = "disease_detail"
        st.rerun()


def diseases_page():
    load_styles()
    render_styles()
    top_bar()

    st.markdown(
        """
        <div class="disease-title">Aprender sobre Bioinformática</div>
        <div class="disease-subtitle">
            Elige una enfermedad genética para explorar su base molecular, secuencias y mutaciones.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        disease_card(DISEASES[0])

    with col2:
        disease_card(DISEASES[1])

    with col3:
        disease_card(DISEASES[2])

    st.divider()

    if st.button("Volver al inicio", key="back_dashboard", type="secondary", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()