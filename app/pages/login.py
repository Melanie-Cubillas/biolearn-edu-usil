import streamlit as st

from components.layout import load_styles, brand_logo
from services.supabase_service import (
    login_user,
    get_profile,
    is_supabase_configured
)


def login_page():
    load_styles()

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        brand_logo()

        st.markdown("<span class='pill'>Bienvenida/o de nuevo 👋</span>", unsafe_allow_html=True)
        st.markdown("<div class='auth-title'>Inicia sesión</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='auth-subtitle'>Continúa explorando genética, mutaciones y secuencias reales desde NCBI.</div>",
            unsafe_allow_html=True
        )

        email = st.text_input("Correo institucional", placeholder="ejemplo@usil.pe")
        password = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")

        if st.button("Ingresar a BioLearn"):
            if not email or not password:
                st.warning("Completa tu correo y contraseña.")
            elif not is_supabase_configured():
                st.error("Supabase no está configurado. Revisa el archivo .env")
            else:
                try:
                    auth = login_user(email, password)
                    user = auth["user"]
                    session = auth["session"]

                    profile = get_profile(
                        user.id,
                        session.access_token,
                        session.refresh_token
                    )

                    st.session_state.user = {
                        "id": user.id,
                        "name": profile.get("full_name", email.split("@")[0]),
                        "email": email,
                        "access_token": session.access_token,
                        "refresh_token": session.refresh_token
                    }

                    st.session_state.page = "dashboard"
                    st.rerun()

                except Exception as error:
                    st.error("No se pudo iniciar sesión.")
                    st.code(str(error))

        if st.button("Crear una cuenta nueva"):
            st.session_state.page = "register"
            st.rerun()

        st.caption("¿Olvidaste tu contraseña? Próximamente agregaremos recuperación por correo.")

    with col2:
        st.markdown("<div class='auth-title'>Aprende bioinformática con datos reales.</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='auth-subtitle'>BioLearn te guía paso a paso para comprender ADN, ARN, traducción, transcripción y reconocimiento de mutaciones.</div>",
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class='soft-box'>🧬 <b>Secuencias reales desde NCBI</b><br>Consulta genes mediante Accession ID y guarda archivos FASTA localmente.</div>
        <div class='soft-box'>🔬 <b>Mutaciones explicadas paso a paso</b><br>Compara secuencias y entiende sustituciones, inserciones, deleciones y patrones genéticos.</div>
        <div class='soft-box'>🎓 <b>Ideal para estudiantes universitarios</b><br>Aprende con ejemplos visuales, quiz interactivo y tutoriales guiados.</div>
        """, unsafe_allow_html=True)