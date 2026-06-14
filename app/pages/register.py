import streamlit as st
from services.supabase_service import supabase


def is_academic_email(email):
    email = email.strip().lower()

    if "@" not in email:
        return False

    domain = email.split("@")[-1]

    return domain.endswith(".edu") or domain.endswith(".edu.pe") or domain.endswith("usil.pe")


def register_page():
    st.title("Crear cuenta")

    full_name = st.text_input("Nombre completo")
    email = st.text_input("Correo institucional")
    university = st.text_input("Universidad")
    password = st.text_input("Contraseña", type="password")
    confirm_password = st.text_input("Confirmar contraseña", type="password")

    if st.button("Registrarse"):
        if not full_name.strip():
            st.error("Debe ingresar su nombre completo.")
            return

        if not email.strip():
            st.error("Debe ingresar su correo institucional.")
            return

        if not is_academic_email(email):
            st.error("Debe ingresar un correo académico válido (.edu o .edu.pe).")
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

    if st.button("Ya tengo cuenta"):
        st.session_state.page = "login"
        st.rerun()