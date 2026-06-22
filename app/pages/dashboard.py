import streamlit as st

from components.layout import load_styles, top_bar


def module_card(icon, title, description, badge, bg_color, border_color, target_page, button_text, progress_value):
    st.markdown(
        f"""
        <div class="module-card" style="background:{bg_color}; border:1px solid {border_color};">
            <div class="module-icon" style="font-size: 13px; font-weight: 800; color: #4F46E5;">{icon}</div>
            <div class="module-arrow">↗</div>
            <div>
                <h3 style="margin-top: 10px; margin-bottom: 5px;">{title}</h3>
                <p>{description}</p>
            </div>
            <span class="module-badge">{badge}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(button_text, use_container_width=True, key=target_page):
        new_progress = max(st.session_state.get("progress", 0), progress_value)
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
        st.session_state.page = target_page
        st.rerun()


def dashboard_page():
    load_styles()
    top_bar()

    user = st.session_state.get("user", {})
    name = user.get("name", "Estudiante") if isinstance(user, dict) else "Estudiante"

    progress = st.session_state.get("progress", 0)
    streak = st.session_state.get("streak", 0)
    badges = st.session_state.get("badges", 0)

    if progress == 0:
        next_goal_text = "Comienza el módulo de Bioinformática para desbloquear tu primera insignia."
    elif progress < 40:
        next_goal_text = "Continúa explorando las enfermedades genéticas y sus secuencias."
    elif progress < 70:
        next_goal_text = "Completa el quiz para reforzar tus conocimientos."
    else:
        next_goal_text = "Finaliza el módulo de Mutaciones para obtener la insignia avanzada."

    st.markdown("""
    <style>
    .dash-user {
        font-weight: 800;
        color: #334155;
    }

    .hero {
        background: linear-gradient(135deg, #DFF4FF 0%, #EEE7FF 55%, #DCFCE7 100%);
        border-radius: 24px;
        padding: 2.5rem;
        margin-bottom: 2.5rem;
        display: grid;
        grid-template-columns: 1.5fr 1.2fr;
        gap: 2rem;
        align-items: center;
        border: 1px solid rgba(226, 232, 240, 0.8);
    }

    .hero-pill {
        display: inline-block;
        background: white;
        padding: 0.4rem 1rem;
        border-radius: 999px;
        font-weight: 700;
        color: #334155;
        font-size: 13px;
        margin-bottom: 1rem;
        border: 1px solid rgba(226, 232, 240, 0.6);
    }

    .hero h1 {
        font-size: 38px;
        line-height: 1.15;
        margin: 0;
        color: #0F172A;
        font-weight: 800;
    }

    .hero p {
        color: #475569;
        font-size: 16px;
        line-height: 1.6;
        margin-top: 1rem;
        margin-bottom: 0;
    }

    .stats {
        display: grid;
        grid-template-columns: repeat(3, minmax(100px, 1fr));
        gap: 1rem;
    }

    .stat-card {
        background: rgba(255, 255, 255, 0.88);
        border-radius: 16px;
        padding: 1.2rem;
        min-height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.03);
        border: 1px solid rgba(226, 232, 240, 0.5);
    }

    .stat-card h2 {
        margin: 0;
        color: #0F172A;
        font-size: 28px;
        font-weight: 800;
    }

    .stat-card span {
        color: #64748B;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: .08em;
        margin-top: .4rem;
    }

    .section-label {
        font-size: 14px;
        letter-spacing: .12em;
        color: #475569;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        text-transform: uppercase;
    }

    .module-card {
        min-height: 240px;
        border-radius: 20px;
        padding: 1.5rem;
        position: relative;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.03);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .module-card h3 {
        font-size: 20px;
        line-height: 1.25;
        color: #0F172A;
        font-weight: 700;
    }

    .module-card p {
        color: #475569;
        font-size: 14px;
        line-height: 1.5;
        margin: 0;
    }

    .module-icon {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.85);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .module-arrow {
        position: absolute;
        top: 1.5rem;
        right: 1.5rem;
        font-size: 20px;
        color: #64748B;
    }

    .module-badge {
        width: fit-content;
        background: white;
        border: 1px solid #E2E8F0;
        padding: .3rem .75rem;
        border-radius: 999px;
        color: #475569;
        font-size: 12px;
        font-weight: 600;
    }

    .activity-card, .goal-card {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 1.5rem;
        min-height: 220px;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.03);
    }

    .activity-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0;
        color: #0F172A;
        gap: 1rem;
        border-bottom: 1px solid #F1F5F9;
    }

    .activity-tag {
        display: inline-flex;
        padding: 0.25rem 0.5rem;
        background: #E0F2FE;
        color: #1D4ED8;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        margin-right: 0.75rem;
    }

    .progress-bg {
        width: 100%;
        height: 10px;
        background: #E2E8F0;
        border-radius: 999px;
        overflow: hidden;
        margin: 1rem 0;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(135deg, #3B82F6, #8B5CF6);
        border-radius: 999px;
    }

    .empty-activity {
        color: #64748B;
        background: #F8FAFC;
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
        font-size: 14px;
        border: 1px dashed #E2E8F0;
    }

    @media (max-width: 1000px) {
        .hero {
            grid-template-columns: 1fr;
            padding: 2rem;
        }

        .stats {
            grid-template-columns: repeat(3, 1fr);
        }

        .hero h1 {
            font-size: 30px;
        }
    }

    @media (max-width: 700px) {
        .stats {
            grid-template-columns: 1fr;
        }

        .module-card {
            min-height: 220px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="hero">
            <div>
                <div class="hero-pill">Estudiante: {name}</div>
                <h1>Continúa explorando el código de la vida</h1>
                <p>Selecciona un módulo para profundizar en procesos genéticos moleculares y análisis bioinformáticos prácticos.</p>
            </div>
            <div class="stats">
                <div class="stat-card"><h2>{progress}%</h2><span>PROGRESO</span></div>
                <div class="stat-card"><h2>{streak}d</h2><span>RACHA</span></div>
                <div class="stat-card"><h2>{badges}</h2><span>INSIGNIAS</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # SECCIÓN 1: Módulos de Análisis
    st.markdown("<div class='section-label'>Módulos de Análisis</div>", unsafe_allow_html=True)
    col_a1, col_a2, col_a3 = st.columns(3, gap="large")

    with col_a1:
        module_card(
            icon="TRN",
            title="Transcripción de ADN",
            description="Transcribe secuencias de ADN a ARN mensajero (ARNm) e identifica codones de parada.",
            badge="Módulo 1",
            bg_color="#E0F2FE",
            border_color="#BAE6FD",
            target_page="transcription",
            button_text="Iniciar transcripción",
            progress_value=30
        )

    with col_a2:
        module_card(
            icon="TRD",
            title="Traducción de Proteínas",
            description="Convierte secuencias de ARNm en aminoácidos y visualiza las conversiones de codones.",
            badge="Módulo 2",
            bg_color="#F3E8FF",
            border_color="#E9D5FF",
            target_page="translation",
            button_text="Iniciar traducción",
            progress_value=60
        )

    with col_a3:
        module_card(
            icon="MUT",
            title="Reconocimiento de Mutaciones",
            description="Compara secuencias contra una referencia para detectar e interpretar mutaciones.",
            badge="Módulo 3",
            bg_color="#DCFCE7",
            border_color="#BBF7D0",
            target_page="mutation_recognition",
            button_text="Iniciar análisis",
            progress_value=90
        )

    # SECCIÓN 2: Recursos y Autoevaluación
    st.markdown("<div class='section-label'>Recursos y Autoevaluación</div>", unsafe_allow_html=True)
    col_r1, col_r2, col_r3 = st.columns(3, gap="large")

    with col_r1:
        module_card(
            icon="GEN",
            title="Base de Enfermedades",
            description="Explora la base genética molecular de Huntington, anemia falciforme y fibrosis quística.",
            badge="3 Casos Clínicos",
            bg_color="#F8FAFC",
            border_color="#E2E8F0",
            target_page="diseases",
            button_text="Ver enfermedades",
            progress_value=20
        )

    with col_r2:
        module_card(
            icon="EVL",
            title="Quiz Académico",
            description="Prueba tus conocimientos con un banco de preguntas dinámicas y explicaciones.",
            badge="Evaluación",
            bg_color="#FFF7ED",
            border_color="#FFEDD5",
            target_page="quiz",
            button_text="Iniciar quiz",
            progress_value=15
        )

    with col_r3:
        module_card(
            icon="TUT",
            title="Guías y Tutoriales",
            description="Ruta de aprendizaje con conceptos de biología molecular, NCBI y formato FASTA.",
            badge="8 Guías",
            bg_color="#EFF6FF",
            border_color="#DBEAFE",
            target_page="tutorials",
            button_text="Ver tutoriales",
            progress_value=10
        )

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.4, 1], gap="large")

    with left:
        if progress == 0:
            activity_html = """
            <div class="empty-activity">
                Aún no tienes actividad reciente registrada. Comienza un módulo para generar progreso.
            </div>
            """
        else:
            activity_html = """
            <div class="activity-row">
                <div><span class="activity-tag">BIO</span>Iniciaste tu aprendizaje en BioLearn</div>
                <span style="font-size: 13px; color: #64748B;">hoy</span>
            </div>
            """

        st.markdown(
            f"""
            <div class="activity-card">
                <h3 style="margin-top:0; font-size: 20px; font-weight:700;">Actividad reciente</h3>
                {activity_html}
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:
        st.markdown(
            f"""
            <div class="goal-card">
                <h3 style="margin-top:0; font-size: 20px; font-weight:700;">Próximo objetivo</h3>
                <p style="font-size: 14px; color:#475569; margin-bottom: 0.5rem;">{next_goal_text}</p>
                <div class="progress-bg">
                    <div class="progress-fill" style="width:{progress}%;"></div>
                </div>
                <p style="text-align:right;color:#64748B;font-size:13px;margin:0;font-weight:700;">{progress}% completado</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Cerrar sesión", type="secondary", use_container_width=True):
        user = st.session_state.get("user", {})
        if isinstance(user, dict) and "email" in user:
            from services.progress_service import save_user_progress
            save_user_progress(
                user["email"],
                st.session_state.get("progress", 0),
                st.session_state.get("streak", 1),
                st.session_state.get("badges", 0)
            )
        st.session_state.user = None
        st.session_state.progress = 0
        st.session_state.streak = 0
        st.session_state.badges = 0
        st.session_state.page = "login"
        st.rerun()