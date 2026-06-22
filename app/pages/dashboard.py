import streamlit as st

from components.layout import load_styles, top_bar


def module_card(icon_html, title, description, badge, bg_color, border_color, target_page, button_text, progress_value):
    st.markdown(
        f"""
        <div class="module-card" style="background:{bg_color}; border:1px solid {border_color}; display: flex; flex-direction: column; justify-content: space-between; min-height: 240px; border-radius: 20px; padding: 1.5rem; position: relative; box-shadow: 0 4px 15px rgba(15, 23, 42, 0.03);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; width: 100%;">
                {icon_html}
                <div class="module-arrow" style="font-size: 20px; color: #64748B;">↗</div>
            </div>
            <div style="margin-top: 1.2rem; margin-bottom: 1.2rem; flex-grow: 1; display: flex; flex-direction: column; justify-content: center;">
                <h3 style="margin: 0 0 6px 0; font-size: 20px; color: #0F172A; font-weight: 700; line-height: 1.25;">{title}</h3>
                <p style="margin: 0; color: #475569; font-size: 14px; line-height: 1.5;">{description}</p>
            </div>
            <span class="module-badge" style="background: white; border: 1px solid #E2E8F0; padding: .3rem .75rem; border-radius: 999px; color: #475569; font-size: 12px; font-weight: 600; width: fit-content; display: inline-block;">{badge}</span>
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

    # MÓDULOS PRINCIPALES
    st.markdown("<div class='section-label'>Módulos Principales</div>", unsafe_allow_html=True)
    col_m1, col_m2, col_m3 = st.columns(3, gap="large")

    with col_m1:
        book_svg = """<div style="background: #E0F2FE; color: #2563EB; width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
        </div>"""
        module_card(
            icon_html=book_svg,
            title="Aprende sobre Bioinformática",
            description="Explora enfermedades genéticas reales, secuencias de ADN y procesos moleculares.",
            badge="12 lecciones",
            bg_color="#EFF6FF",
            border_color="#DBEAFE",
            target_page="diseases",
            button_text="Ver enfermedades",
            progress_value=20
        )

    with col_m2:
        brain_svg = """<div style="background: #F3E8FF; color: #7C3AED; width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M12 5v14"/></svg>
        </div>"""
        module_card(
            icon_html=brain_svg,
            title="Pon a prueba tus conocimientos",
            description="Quizzes interactivos con preguntas de selección múltiple e interpretación de secuencias.",
            badge="8 evaluaciones",
            bg_color="#FAF5FF",
            border_color="#F3E8FF",
            target_page="quiz",
            button_text="Iniciar quiz",
            progress_value=15
        )

    with col_m3:
        play_svg = """<div style="background: #DCFCE7; color: #16A34A; width: 44px; height: 44px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="10 8 16 12 10 16 10 8"/></svg>
        </div>"""
        module_card(
            icon_html=play_svg,
            title="Tutoriales",
            description="Guías paso a paso de transcripción, traducción y detección de mutaciones.",
            badge="5 tutoriales",
            bg_color="#F0FDF4",
            border_color="#DCFCE7",
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