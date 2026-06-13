import streamlit as st
from components.layout import load_styles, show_logo


def login_page():
    load_styles()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        show_logo(230)

        st.subheader("Inicio de sesión")

        email = st.text_input("Correo institucional")
        password = st.text_input("Contraseña", type="password")

        if st.button("INGRESAR", use_container_width=True):
            if email and password:
                st.session_state.user = {
                    "name": email.split("@")[0],
                    "email": email
                }
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.warning("Ingresa tu correo y contraseña.")

        if st.button("¿No tienes cuenta? Regístrate"):
            st.session_state.page = "register"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.markdown("<h1 class='title'>Bienvenido a BioLearn</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>Aprende bioinformática de forma visual, interactiva y práctica.</p>", unsafe_allow_html=True)
        st.info("Explora enfermedades genéticas, analiza secuencias y reconoce mutaciones.")
        st.markdown("</div>", unsafe_allow_html=True)
