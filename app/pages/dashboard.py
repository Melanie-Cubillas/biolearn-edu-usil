import streamlit as st

from components.layout import load_styles


def module_card(icon, title, description, badge, bg_color, border_color, target_page, button_text, progress_value):
    st.markdown(
        f"""
        <div class="module-card" style="background:{bg_color}; border:1px solid {border_color};">
            <div class="module-icon">{icon}</div>
            <div class="module-arrow">↗</div>
            <div>
                <h3>{title}</h3>
                <p>{description}</p>
            </div>
            <span class="module-badge">{badge}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(button_text, use_container_width=True, key=target_page):
        st.session_state.progress = max(st.session_state.get("progress", 0), progress_value)
        st.session_state.page = target_page
        st.rerun()


def dashboard_page():
    load_styles()

    user = st.session_state.get("user", {})
    name = user.get("name", "Estudiante")

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
    .dashboard-header {
        background: rgba(255,255,255,0.9);
        border-radius: 28px;
        padding: 1.3rem 1.8rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 12px 30px rgba(15,23,42,0.06);
        margin-bottom: 2rem;
    }

    .dash-logo {
        font-size: 26px;
        font-weight: 900;
        color: #0F172A;
    }

    .dash-user {
        font-weight: 800;
        color: #334155;
    }

    .hero {
        background: linear-gradient(135deg, #DFF4FF 0%, #EEE7FF 55%, #DCFCE7 100%);
        border-radius: 34px;
        padding: 3rem;
        margin-bottom: 2.5rem;
        display: grid;
        grid-template-columns: 1.5fr 1.2fr;
        gap: 2rem;
        align-items: center;
    }

    .hero-pill {
        display: inline-block;
        background: white;
        padding: 0.55rem 1rem;
        border-radius: 999px;
        font-weight: 800;
        color: #334155;
        margin-bottom: 1rem;
    }

    .hero h1 {
        font-size: 46px;
        line-height: 1.05;
        margin: 0;
        color: #0F172A;
        font-weight: 900;
    }

    .hero p {
        color: #475569;
        font-size: 19px;
        line-height: 1.6;
        margin-top: 1rem;
    }

    .stats {
        display: grid;
        grid-template-columns: repeat(3, minmax(120px, 1fr));
        gap: 1rem;
    }

    .stat-card {
        background: rgba(255,255,255,0.88);
        border-radius: 24px;
        padding: 1.6rem;
        min-height: 145px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 10px 25px rgba(15,23,42,0.06);
    }

    .stat-card h2 {
        margin: 0;
        color: #0F172A;
        font-size: 32px;
        font-weight: 900;
    }

    .stat-card span {
        color: #64748B;
        font-size: 12px;
        font-weight: 900;
        letter-spacing: .08em;
        margin-top: .5rem;
    }

    .section-label {
        font-size: 18px;
        letter-spacing: .12em;
        color: #475569;
        font-weight: 900;
        margin-bottom: 1rem;
    }

    .module-card {
        min-height: 300px;
        border-radius: 28px;
        padding: 2rem;
        position: relative;
        box-shadow: 0 12px 28px rgba(15,23,42,0.05);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .module-card h3 {
        font-size: 26px;
        line-height: 1.15;
        color: #0F172A;
        margin: 1rem 0 .4rem 0;
    }

    .module-card p {
        color: #5B677A;
        font-size: 16px;
        line-height: 1.45;
        margin: 0;
    }

    .module-icon {
        width: 58px;
        height: 58px;
        border-radius: 20px;
        background: rgba(255,255,255,0.75);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
    }

    .module-arrow {
        position: absolute;
        top: 2rem;
        right: 2rem;
        font-size: 28px;
        color: #64748B;
    }

    .module-badge {
        width: fit-content;
        background: white;
        border: 1px solid #E2E8F0;
        padding: .45rem .9rem;
        border-radius: 999px;
        color: #334155;
        font-size: 14px;
        font-weight: 700;
    }

    .activity-card, .goal-card {
        background: rgba(255,255,255,0.9);
        border: 1px solid #E2E8F0;
        border-radius: 28px;
        padding: 2rem;
        min-height: 300px;
        box-shadow: 0 12px 28px rgba(15,23,42,0.04);
    }

    .activity-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        color: #0F172A;
        gap: 1rem;
    }

    .activity-tag {
        display: inline-flex;
        width: 48px;
        height: 48px;
        border-radius: 999px;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        font-weight: 900;
        margin-right: 1rem;
    }

    .progress-bg {
        width: 100%;
        height: 14px;
        background: #E2E8F0;
        border-radius: 999px;
        overflow: hidden;
        margin: 1.2rem 0;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(135deg, #3B82F6, #8B5CF6);
        border-radius: 999px;
    }

    .empty-activity {
        color: #64748B;
        background: #F8FAFC;
        border-radius: 18px;
        padding: 1rem;
        margin-top: 1rem;
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
            font-size: 34px;
        }
    }

    @media (max-width: 700px) {
        .dashboard-header {
            flex-direction: column;
            align-items: flex-start;
            gap: .7rem;
        }

        .stats {
            grid-template-columns: 1fr;
        }

        .module-card {
            min-height: 260px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="dashboard-header">
            <div class="dash-logo">BioLearn 🧬</div>
            <div class="dash-user">👤 {name}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="hero">
            <div>
                <div class="hero-pill">Hola, {name} 👋</div>
                <h1>Continúa explorando el código de la vida.</h1>
                <p>Selecciona un módulo para profundizar en genética, mutaciones y procesos bioinformáticos reales.</p>
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

    st.markdown("<div class='section-label'>MÓDULOS PRINCIPALES</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        module_card(
            icon="📘",
            title="Aprende sobre Bioinformática",
            description="Explora enfermedades genéticas reales, secuencias de ADN y procesos moleculares.",
            badge="3 lecciones",
            bg_color="#E0F2FE",
            border_color="#BAE6FD",
            target_page="diseases",
            button_text="Ingresar",
            progress_value=10
        )

    with col2:
        module_card(
            icon="🧠",
            title="Pon a prueba tus conocimientos",
            description="Quizzes interactivos con preguntas aleatorias del banco de preguntas.",
            badge="5 preguntas",
            bg_color="#F3E8FF",
            border_color="#E9D5FF",
            target_page="quiz",
            button_text="Ir al quiz",
            progress_value=20
        )

    with col3:
        module_card(
            icon="▶️",
            title="Tutoriales",
            description="Guías paso a paso de transcripción, traducción y detección de mutaciones.",
            badge="5 tutoriales",
            bg_color="#DCFCE7",
            border_color="#BBF7D0",
            target_page="tutorials",
            button_text="Ver tutoriales",
            progress_value=15
        )

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.4, 1], gap="large")

    with left:
        if progress == 0:
            activity_html = """
            <div class="empty-activity">
                Aún no tienes actividad registrada. Empieza con el módulo de Bioinformática para generar tu primer avance.
            </div>
            """
        else:
            activity_html = """
            <div class="activity-row">
                <div><span class="activity-tag" style="background:#E0F2FE;">BIO</span>Iniciaste tu aprendizaje en BioLearn</div>
                <span>hoy</span>
            </div>
            """

        st.markdown(
            f"""
            <div class="activity-card">
                <h3>Actividad reciente</h3>
                {activity_html}
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:
        st.markdown(
            f"""
            <div class="goal-card">
                <h3>Próximo objetivo</h3>
                <p>{next_goal_text}</p>
                <div class="progress-bg">
                    <div class="progress-fill" style="width:{progress}%;"></div>
                </div>
                <p style="text-align:right;color:#64748B;">{progress}%</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Continuar", use_container_width=True):
            st.session_state.progress = max(st.session_state.get("progress", 0), 10)
            st.session_state.page = "diseases"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Cerrar sesión"):
        st.session_state.user = None
        st.session_state.progress = 0
        st.session_state.streak = 0
        st.session_state.badges = 0
        st.session_state.page = "login"
        st.rerun()