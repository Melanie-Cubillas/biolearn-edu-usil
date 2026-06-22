import streamlit as st

from components.layout import load_styles, top_bar


def module_card(icon, title, description, badge, bg_color, border_color, target_page, button_text):
    st.html(f"""
    <div class="module-card" style="background:{bg_color}; border:1px solid {border_color};">
        <div class="module-top">
            <div class="module-icon">{icon}</div>
            <div class="module-arrow">↗</div>
        </div>

        <div class="module-content">
            <h3>{title}</h3>
            <p>{description}</p>
        </div>

        <span class="module-badge">{badge}</span>
    </div>
    """)

    if st.button(button_text, use_container_width=True, key=target_page):
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
        next_goal_text = "Continúa explorando enfermedades genéticas y sus secuencias."
    elif progress < 70:
        next_goal_text = "Completa el quiz para reforzar tus conocimientos."
    else:
        next_goal_text = "Finaliza el módulo de Mutaciones para obtener la insignia avanzada."

    st.html("""
    <style>
    .hero {
        background: linear-gradient(135deg, #DFF4FF 0%, #EEE7FF 55%, #DCFCE7 100%);
        border-radius: 28px;
        padding: 2.7rem;
        margin-bottom: 2.5rem;
        display: grid;
        grid-template-columns: 1.2fr 1fr;
        gap: 2rem;
        align-items: center;
        border: 1px solid rgba(226,232,240,.8);
    }

    .hero-pill {
        display: inline-block;
        background: white;
        padding: .45rem 1.1rem;
        border-radius: 999px;
        font-weight: 800;
        color: #334155;
        font-size: 13px;
        margin-bottom: 1.2rem;
    }

    .hero h1 {
        font-size: 42px;
        line-height: 1.15;
        margin: 0;
        color: #0F172A;
        font-weight: 900;
    }

    .hero p {
        color: #475569;
        font-size: 17px;
        line-height: 1.6;
        margin-top: 1.2rem;
    }

    .stats {
        display: grid;
        grid-template-columns: repeat(3, minmax(145px, 1fr));
        gap: 1rem;
    }

    .stat-card {
        border-radius: 18px;
        height: 145px;
        padding: 1rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: .55rem;
        text-align: center;
        color: white;
        box-shadow: 0 12px 28px rgba(2,6,23,.22);
        overflow: hidden;
    }

    .progress-card { background: linear-gradient(135deg, #071232, #0B2454); }
    .streak-card { background: linear-gradient(135deg, #0B2454, #3B82F6); }
    .badge-card { background: linear-gradient(135deg, #3B0066, #7C3AED); }

    .metric-icon {
        width: 46px;
        height: 46px;
        border-radius: 14px;
        background: rgba(255,255,255,.14);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
    }

    .metric-value {
        font-size: 25px;
        font-weight: 900;
        line-height: 1;
        color: white;
    }

    .metric-label {
        font-size: 11px;
        font-weight: 900;
        letter-spacing: .06em;
        color: rgba(255,255,255,.9);
        white-space: nowrap;
    }

    .section-label {
        font-size: 14px;
        letter-spacing: .12em;
        color: #475569;
        font-weight: 900;
        margin: 1.5rem 0 1rem 0;
        text-transform: uppercase;
    }

    .module-card {
        min-height: 250px;
        border-radius: 24px;
        padding: 1.6rem;
        box-shadow: 0 8px 24px rgba(15,23,42,.04);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
    }

    .module-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }

    .module-icon {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: white;
        font-size: 24px;
    }

    .module-arrow {
        font-size: 22px;
        color: #64748B;
        font-weight: 900;
    }

    .module-content {
        margin: 1.2rem 0;
    }

    .module-content h3 {
        margin: 0 0 .7rem 0;
        font-size: 22px;
        line-height: 1.25;
        color: #0F172A;
        font-weight: 900;
    }

    .module-content p {
        color: #475569;
        font-size: 15px;
        line-height: 1.55;
        margin: 0;
    }

    .module-badge {
        width: fit-content;
        background: white;
        border: 1px solid #E2E8F0;
        padding: .35rem .85rem;
        border-radius: 999px;
        color: #475569;
        font-size: 12px;
        font-weight: 800;
    }

    .activity-card, .goal-card {
        background: rgba(255,255,255,.9);
        border: 1px solid #E2E8F0;
        border-radius: 22px;
        padding: 1.5rem;
        min-height: 220px;
        box-shadow: 0 8px 24px rgba(15,23,42,.04);
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

    .activity-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: .75rem 0;
        color: #0F172A;
        border-bottom: 1px solid #F1F5F9;
    }

    .activity-tag {
        display: inline-flex;
        padding: .25rem .5rem;
        background: #E0F2FE;
        color: #1D4ED8;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 800;
        margin-right: .75rem;
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

    @media (max-width: 1100px) {
        .hero {
            grid-template-columns: 1fr;
            padding: 2rem;
        }

        .stats {
            grid-template-columns: repeat(3, minmax(130px, 1fr));
        }

        .hero h1 {
            font-size: 34px;
        }
    }

    @media (max-width: 700px) {
        .stats {
            grid-template-columns: 1fr;
        }

        .hero h1 {
            font-size: 30px;
        }
    }
    </style>
    """)

    st.html(f"""
    <div class="hero">
        <div>
            <div class="hero-pill">Estudiante: {name}</div>
            <h1>Continúa explorando el código de la vida</h1>
            <p>Selecciona un módulo para profundizar en procesos genéticos moleculares y análisis bioinformáticos prácticos.</p>
        </div>

        <div class="stats">
            <div class="stat-card progress-card">
                <div class="metric-icon">⏱️</div>
                <div class="metric-value">{progress}%</div>
                <div class="metric-label">PROGRESO</div>
            </div>

            <div class="stat-card streak-card">
                <div class="metric-icon">🔥</div>
                <div class="metric-value">{streak}d</div>
                <div class="metric-label">RACHA</div>
            </div>

            <div class="stat-card badge-card">
                <div class="metric-icon">⭐</div>
                <div class="metric-value">{badges}</div>
                <div class="metric-label">INSIGNIAS</div>
            </div>
        </div>
    </div>
    """)

    st.html("<div class='section-label'>Módulos Principales</div>")

    col_m1, col_m2, col_m3 = st.columns(3, gap="large")

    with col_m1:
        module_card(
            icon="📘",
            title="Aprende sobre Bioinformática",
            description="Explora enfermedades genéticas reales, secuencias de ADN y procesos moleculares.",
            badge="12 lecciones",
            bg_color="#EFF6FF",
            border_color="#DBEAFE",
            target_page="diseases",
            button_text="Ver enfermedades"
        )

    with col_m2:
        module_card(
            icon="🧠",
            title="Pon a prueba tus conocimientos",
            description="Quizzes interactivos con preguntas de selección múltiple e interpretación de secuencias.",
            badge="8 evaluaciones",
            bg_color="#FAF5FF",
            border_color="#F3E8FF",
            target_page="quiz",
            button_text="Iniciar quiz"
        )

    with col_m3:
        module_card(
            icon="▶️",
            title="Tutoriales",
            description="Guías paso a paso de transcripción, traducción y detección de mutaciones.",
            badge="5 tutoriales",
            bg_color="#F0FDF4",
            border_color="#DCFCE7",
            target_page="tutorials",
            button_text="Ver tutoriales"
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
                <span style="font-size:13px;color:#64748B;">hoy</span>
            </div>
            """

        st.html(f"""
        <div class="activity-card">
            <h3 style="margin-top:0;font-size:20px;font-weight:900;">Actividad reciente</h3>
            {activity_html}
        </div>
        """)

    with right:
        st.html(f"""
        <div class="goal-card">
            <h3 style="margin-top:0;font-size:20px;font-weight:900;">Próximo objetivo</h3>
            <p style="font-size:14px;color:#475569;margin-bottom:.5rem;">{next_goal_text}</p>
            <div class="progress-bg">
                <div class="progress-fill" style="width:{progress}%;"></div>
            </div>
            <p style="text-align:right;color:#64748B;font-size:13px;margin:0;font-weight:800;">{progress}% completado</p>
        </div>
        """)

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