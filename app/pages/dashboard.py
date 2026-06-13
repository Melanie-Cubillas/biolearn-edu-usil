import streamlit as st
from components.layout import load_styles, top_bar
from components.cards import option_card


def dashboard_page():
    load_styles()
    top_bar()

    user = st.session_state.get("user", {})
    name = user.get("name", "estudiante")

    st.markdown(f"<h1 class='title'>Hola {name}, ¿qué te gustaría realizar?</h1>", unsafe_allow_html=True)
    st.write("Selecciona una opción para comenzar tu aprendizaje.")

    col1, col2, col3 = st.columns(3)

    with col1:
        option_card(
            "Aprende sobre Bioinformática",
            "Explora enfermedades genéticas y analiza secuencias reales.",
            "Ingresar",
            "diseases"
        )

    with col2:
        option_card(
            "Pon a prueba tus conocimientos",
            "Resuelve preguntas interactivas sobre ADN, ARN y mutaciones.",
            "Ir al quiz",
            "quiz"
        )

    with col3:
        option_card(
            "Tutoriales",
            "Aprende paso a paso cómo usar la plataforma.",
            "Ver tutoriales",
            "tutorials"
        )

    if st.button("Cerrar sesión"):
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()
