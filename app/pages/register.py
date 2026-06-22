import streamlit as st

from components.layout import load_styles, brand_logo
from services.supabase_service import supabase, is_supabase_configured


def is_academic_email(email):
    email = email.strip().lower()

    if "@" not in email:
        return False

    domain = email.split("@")[-1]

    return (
        domain.endswith(".edu")
        or domain.endswith(".edu.pe")
        or domain.endswith("usil.pe")
    )


def register_page():
    load_styles()

    col1, col2 = st.columns([0.9, 1.1], gap="large")

    with col1:
        brand_logo()

        st.markdown("<span class='pill'>Primer paso</span>", unsafe_allow_html=True)
        st.markdown("<div class='auth-title'>Crea tu cuenta BioLearn</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='auth-subtitle'>Únete a una experiencia educativa para aprender bioinformática de forma práctica, visual y aplicada.</div>",
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class='soft-box'>
        Tu cuenta guardará tu progreso, tus resultados del quiz y tus avances por módulo.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        with st.container(border=True):
            st.markdown("<div class='auth-title'>Registro</div>", unsafe_allow_html=True)

            full_name = st.text_input("Nombre completo", placeholder="María González")
            email = st.text_input("Correo institucional", placeholder="nombre@usil.pe")
            university = st.text_input("Universidad", placeholder="USIL")
            password = st.text_input("Contraseña", type="password", placeholder="Crea una contraseña")
            confirm_password = st.text_input("Confirmar contraseña", type="password", placeholder="Repite tu contraseña")

            if st.button("Crear cuenta", type="primary", use_container_width=True):
                if not full_name.strip():
                    st.error("Debe ingresar su nombre completo.")
                    return

                if not email.strip():
                    st.error("Debe ingresar su correo institucional.")
                    return

                if not is_academic_email(email):
                    st.error("Debe ingresar un correo académico válido (.edu, .edu.pe o usil.pe).")
                    return

                if not university.strip():
                    st.error("Debe ingresar su universidad.")
                    return

                if not password:
                    st.error("Debe ingresar una contraseña.")
                    return

                if password != confirm_password:
                    st.error("Las contraseñas no coinciden.")
                    return

                if not is_supabase_configured():
                    st.error("Supabase no está configurado. Revisa el archivo .env")
                    return

                try:
                    supabase.auth.sign_up({
                        "email": email,
                        "password": password,
                        "options": {
                            "data": {
                                "full_name": full_name,
                                "university": university
                            }
                        }
                    })

                    st.success("Registro exitoso. Revisa tu correo para confirmar tu cuenta.")
                    st.session_state.page = "login"
                    st.rerun()

                except Exception as e:
                    st.error(f"Error al registrar usuario: {e}")

            if st.button("Ya tengo cuenta", type="secondary", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()