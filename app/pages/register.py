import streamlit as st
from components.layout import load_styles, show_logo


def register_page():
    load_styles()

    st.markdown("<div class='main-card'>", unsafe_allow_html=True)

    show_logo(220)
    st.title("Crear cuenta")

    name = st.text_input("Nombre completo")
    email = st.text_input("Correo institucional")
    password = st.text_input("Contraseña", type="password")
    confirm_password = st.text_input("Confirmar contraseña", type="password")

    if st.button("REGISTRARME", use_container_width=True):
        if not name or not email or not password:
            st.warning("Completa todos los campos.")
        elif password != confirm_password:
            st.error("Las contraseñas no coinciden.")
        else:
            st.success("Cuenta creada correctamente.")
            st.session_state.user = {
                "name": name,
                "email": email
            }
            st.session_state.page = "dashboard"
            st.rerun()

    if st.button("Volver al login"):
        st.session_state.page = "login"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
