import streamlit as st

from components.layout import load_styles, brand_logo
from services.supabase_service import (
    login_user,
    get_profile,
    is_supabase_configured,
    reset_password
)


def login_page():
    load_styles()

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        brand_logo()

        with st.container(border=True):
            if st.session_state.get("forgot_password", False):
                st.markdown("<span class='pill'>Recuperación de cuenta</span>", unsafe_allow_html=True)
                st.markdown("<div class='auth-title'>Restablecer contraseña</div>", unsafe_allow_html=True)
                st.markdown(
                    "<div class='auth-subtitle'>Ingresa tu correo institucional registrado y te enviaremos un enlace seguro para restablecer tu contraseña.</div>",
                    unsafe_allow_html=True
                )

                recovery_email = st.text_input("Correo institucional", placeholder="ejemplo@usil.pe", key="recovery_email")

                if st.session_state.get("password_reset_sent", False):
                    st.success("Correo enviado: revisa tu bandeja de entrada y la carpeta de spam.")
                    st.info("El enlace de restablecimiento llegará en breve. Si no lo ves, espera unos minutos o solicita nuevamente.")

                    if st.button("Volver al inicio de sesión", type="secondary", use_container_width=True):
                        st.session_state.forgot_password = False
                        st.session_state.password_reset_sent = False
                        st.session_state.recovery_email = ""
                        st.rerun()
                else:
                    if st.button("Enviar instrucciones", type="primary", use_container_width=True):
                        if not recovery_email.strip():
                            st.error("Por favor, ingresa tu correo institucional para continuar.")
                        elif not is_supabase_configured():
                            st.error("Supabase no está configurado. Revisa el archivo .env")
                        else:
                            try:
                                reset_password(recovery_email.strip())
                                st.session_state.password_reset_sent = True
                                st.success("Solicitud recibida. Te enviaremos un correo si este correo está registrado en la plataforma.")
                                st.info("Revisa tu bandeja de entrada y la carpeta de spam.")
                            except Exception as e:
                                st.error(f"No fue posible enviar el enlace. Verifica tu conexión e inténtalo de nuevo.")
                                st.code(str(e))

                    if st.button("Volver al inicio de sesión", type="secondary", use_container_width=True):
                        st.session_state.forgot_password = False
                        st.session_state.password_reset_sent = False
                        st.session_state.recovery_email = ""
                        st.rerun()
            else:
                st.markdown("<span class='pill'>Bienvenida/o de nuevo</span>", unsafe_allow_html=True)
                st.markdown("<div class='auth-title'>Inicia sesión</div>", unsafe_allow_html=True)
                st.markdown(
                    "<div class='auth-subtitle'>Continúa explorando genética, mutaciones y secuencias reales desde NCBI.</div>",
                    unsafe_allow_html=True
                )

                email = st.text_input("Correo institucional", placeholder="ejemplo@usil.pe")
                password = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")

                if st.button("Ingresar a BioLearn", type="primary", use_container_width=True):
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

                            from services.progress_service import load_user_progress
                            progress, streak, badges = load_user_progress(email)
                            st.session_state.progress = progress
                            st.session_state.streak = streak
                            st.session_state.badges = badges

                            st.session_state.page = "dashboard"
                            st.rerun()

                        except Exception as error:
                            st.error("No se pudo iniciar sesión. Verifica tus credenciales.")

                if st.button("Crear una cuenta nueva", type="secondary", use_container_width=True):
                    st.session_state.page = "register"
                    st.rerun()

                if st.button("¿Olvidaste tu contraseña?", key="forgot_password_btn", use_container_width=True):
                    st.session_state.forgot_password = True
                    st.rerun()

    with col2:
        st.html("""
        <div class="dna-illustration-container">
            <svg class="dna-helix-svg" viewBox="0 0 400 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="dnaGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#3B82F6" stop-opacity="0.85"/>
                        <stop offset="100%" stop-color="#8B5CF6" stop-opacity="0.85"/>
                    </linearGradient>
                    <linearGradient id="dnaLineGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#93C5FD" stop-opacity="0.3"/>
                        <stop offset="100%" stop-color="#C084FC" stop-opacity="0.3"/>
                    </linearGradient>
                </defs>
                <path d="M 20 60 Q 70 10, 120 60 T 220 60 T 320 60 T 420 60" stroke="url(#dnaGrad)" stroke-width="3.5" stroke-dasharray="2,2"/>
                <path d="M 20 60 Q 70 110, 120 60 T 220 60 T 320 60 T 420 60" stroke="url(#dnaGrad)" stroke-width="3.5" opacity="0.5"/>
                <line x1="45" y1="40" x2="45" y2="80" stroke="url(#dnaLineGrad)" stroke-width="2.5"/>
                <line x1="95" y1="78" x2="95" y2="42" stroke="url(#dnaLineGrad)" stroke-width="2.5"/>
                <line x1="145" y1="40" x2="145" y2="80" stroke="url(#dnaLineGrad)" stroke-width="2.5"/>
                <line x1="195" y1="78" x2="195" y2="42" stroke="url(#dnaLineGrad)" stroke-width="2.5"/>
                <line x1="245" y1="40" x2="245" y2="80" stroke="url(#dnaLineGrad)" stroke-width="2.5"/>
                <line x1="295" y1="78" x2="295" y2="42" stroke="url(#dnaLineGrad)" stroke-width="2.5"/>
                <line x1="345" y1="40" x2="345" y2="80" stroke="url(#dnaLineGrad)" stroke-width="2.5"/>
                <circle cx="45" cy="40" r="5" fill="#3B82F6"/>
                <circle cx="45" cy="80" r="5" fill="#8B5CF6"/>
                <circle cx="95" cy="78" r="5" fill="#3B82F6"/>
                <circle cx="95" cy="42" r="5" fill="#8B5CF6"/>
                <circle cx="145" cy="40" r="5" fill="#3B82F6"/>
                <circle cx="145" cy="80" r="5" fill="#8B5CF6"/>
                <circle cx="195" cy="78" r="5" fill="#3B82F6"/>
                <circle cx="195" cy="42" r="5" fill="#8B5CF6"/>
                <circle cx="245" cy="40" r="5" fill="#3B82F6"/>
                <circle cx="245" cy="80" r="5" fill="#8B5CF6"/>
                <circle cx="295" cy="78" r="5" fill="#3B82F6"/>
                <circle cx="295" cy="42" r="5" fill="#8B5CF6"/>
                <circle cx="345" cy="40" r="5" fill="#3B82F6"/>
                <circle cx="345" cy="80" r="5" fill="#8B5CF6"/>
            </svg>
        </div>
        """)

        st.markdown("<div class='auth-title'>Aprende bioinformática con datos reales</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='auth-subtitle'>BioLearn te guía paso a paso para comprender ADN, ARN, traducción, transcripción y reconocimiento de mutaciones.</div>",
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class='hero-card'>
            <div class='hero-card-icon' style='font-size: 13px; font-weight: 800; color: #4F46E5;'>DNA</div>
            <div class='hero-card-content'>
                <div class='hero-card-title'>Secuencias reales desde NCBI</div>
                <div class='hero-card-desc'>Consulta genes mediante Accession ID y guarda archivos FASTA localmente de forma rápida e intuitiva.</div>
            </div>
        </div>
        <div class='hero-card'>
            <div class='hero-card-icon' style='font-size: 13px; font-weight: 800; color: #4F46E5;'>MUT</div>
            <div class='hero-card-content'>
                <div class='hero-card-title'>Mutaciones explicadas paso a paso</div>
                <div class='hero-card-desc'>Compara secuencias y entiende sustituciones, inserciones, deleciones y patrones genéticos con explicaciones claras.</div>
            </div>
        </div>
        <div class='hero-card'>
            <div class='hero-card-icon' style='font-size: 13px; font-weight: 800; color: #4F46E5;'>EDU</div>
            <div class='hero-card-content'>
                <div class='hero-card-title'>Ideal para estudiantes universitarios</div>
                <div class='hero-card-desc'>Aprende con ejemplos visuales, un quiz interactivo de autoevaluación y tutoriales guiados.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)