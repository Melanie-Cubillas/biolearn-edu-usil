import random
import streamlit as st

from components.layout import load_styles, top_bar
from services.supabase_service import (
    is_supabase_configured,
    get_quiz_questions,
    save_quiz_result
)


def get_mastery_rank(score: int, total: int) -> dict:
    ratio = score / total if total else 0

    if ratio == 1:
        return {
            "title": "Especialista en Genomas",
            "subtitle": "Tu dominio es sobresaliente. Has alcanzado el nivel máximo de maestría bioinformática.",
            "badge": "Maestría total",
            "tone": "success"
        }
    if ratio >= 0.8:
        return {
            "title": "Investigador Junior",
            "subtitle": "Buen trabajo. Sigue avanzando para convertirte en un experto del ADN.",
            "badge": "Nivel avanzado",
            "tone": "info"
        }
    if ratio >= 0.6:
        return {
            "title": "Analista Experimental",
            "subtitle": "Vas por muy buen camino. Repasa un poco para consolidar los conceptos.",
            "badge": "En ascenso",
            "tone": "info"
        }
    if ratio >= 0.4:
        return {
            "title": "Explorador de Secuencias",
            "subtitle": "Tienes bases sólidas. Identifica las áreas con más dudas y refuerza tu aprendizaje.",
            "badge": "Potencial detectado",
            "tone": "warning"
        }
    return {
        "title": "Aprendiz de ADN",
        "subtitle": "Cada intento construye experiencia. Usa la sección de revisión para avanzar rápido.",
        "badge": "Inicio de viaje",
        "tone": "warning"
    }


def quiz_page():
    load_styles()
    top_bar()

    st.title("Pon a prueba tus conocimientos")
    st.write("Responde preguntas aleatorias del banco de preguntas.")

    if not is_supabase_configured():
        st.error("Supabase no está configurado. Revisa el archivo .env")
        return

    user = st.session_state.get("user")

    if not user:
        st.warning("Debes iniciar sesión para resolver el quiz.")
        if st.button("Ir al login"):
            st.session_state.page = "login"
            st.rerun()
        return

    try:
        if "quiz_questions" not in st.session_state:
            questions = get_quiz_questions(limit=5)

            for question in questions:
                options = question.get("quiz_options", []).copy()
                random.shuffle(options)
                question["quiz_options"] = options

            st.session_state.quiz_questions = questions
            st.session_state.quiz_submitted = False

        questions = st.session_state.quiz_questions

        if not questions:
            st.warning("No hay preguntas registradas en Supabase.")
            return

        selected_answers = {}
        unanswered_questions = []

        for index, question in enumerate(questions):
            st.markdown(f"### Pregunta {index + 1}")
            st.write(question["question"])

            topic = question.get("topic", "General")
            difficulty = question.get("difficulty", "Básico")
            st.caption(f"Tema: {topic} | Nivel: {difficulty}")

            options = question.get("quiz_options", [])

            option_map = {
                option["option_text"]: option
                for option in options
            }

            saved_val = st.session_state.get(f"question_{question['id']}")
            try:
                saved_idx = list(option_map.keys()).index(saved_val) if saved_val is not None else None
            except ValueError:
                saved_idx = None

            st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)
            st.markdown("<style>.stRadio > label { display: none; }</style>", unsafe_allow_html=True)
            
            selected_label = st.radio(
                "Selecciona una respuesta",
                list(option_map.keys()),
                index=saved_idx,
                disabled=st.session_state.quiz_submitted,
                key=f"question_{question['id']}",
                label_visibility="collapsed"
            )

            if selected_label is None and saved_val is None:
                unanswered_questions.append(index + 1)
            elif selected_label or saved_val:
                final_selection = selected_label or saved_val
                if final_selection in option_map:
                    selected_answers[question["id"]] = option_map[final_selection]

            if st.session_state.quiz_submitted:
                user_opt = option_map.get(saved_val) if saved_val else None
                if user_opt:
                    if user_opt["is_correct"]:
                        st.success("✅ Respuesta correcta")
                    else:
                        st.error("❌ Respuesta incorrecta")
                        correct_opt = next((o for o in options if o["is_correct"]), None)
                        if correct_opt:
                            st.info(f"✓ Respuesta correcta: {correct_opt['option_text']}")
                else:
                    st.warning("⚠️ No respondiste esta pregunta.")

                st.markdown(f"**Explicación:** {question.get('explanation', 'Sin explicación disponible.')}")
                st.divider()

        col1, col2 = st.columns(2)

        with col1:
            if not st.session_state.quiz_submitted:
                if st.button("Enviar respuestas", type="primary", use_container_width=True):
                    if unanswered_questions:
                        st.warning(
                            "Debes responder todas las preguntas antes de enviar. "
                            f"Faltan: {', '.join(map(str, unanswered_questions))}."
                        )
                        return

                    score = 0

                    for selected_option in selected_answers.values():
                        if selected_option["is_correct"]:
                            score += 1

                    total = len(questions)

                    save_quiz_result(
                        user_id=user["id"],
                        score=score,
                        total_questions=total,
                        access_token=user["access_token"],
                        refresh_token=user["refresh_token"]
                    )

                    st.session_state.quiz_score = score
                    st.session_state.quiz_total = total
                    st.session_state.quiz_submitted = True

                    # Actualizar progreso e insignias
                    # Grant progress only once per user action (quiz submission).
                    if not st.session_state.get("completed_quiz", False):
                        increment = 20
                        st.session_state.progress = min(100, st.session_state.get("progress", 0) + increment)
                        st.session_state.completed_quiz = True

                    new_progress = st.session_state.get("progress", 0)

                    new_badges = st.session_state.get("badges", 0)
                    if score == total:
                        new_badges = max(new_badges, 1)
                        st.session_state.badges = new_badges

                    user = st.session_state.get("user", {})
                    if isinstance(user, dict) and "email" in user:
                        from services.progress_service import save_user_progress
                        save_user_progress(
                            user["email"],
                            new_progress,
                            st.session_state.get("streak", 1),
                            new_badges
                        )

                    st.rerun()
            else:
                st.info(f"Puntaje obtenido: {st.session_state.quiz_score}/{st.session_state.quiz_total}")

        with col2:
            if st.button("Generar nuevas preguntas", type="secondary", use_container_width=True):
                st.session_state.pop("quiz_questions", None)
                st.session_state.pop("quiz_score", None)
                st.session_state.pop("quiz_total", None)
                st.session_state.quiz_submitted = False
                st.rerun()

        if st.session_state.get("quiz_submitted"):
            score = st.session_state.quiz_score
            total = st.session_state.quiz_total
            rank = get_mastery_rank(score, total)

            st.markdown(
                f"""
                <div class='quiz-rank-card'>
                    <div style='display:flex; align-items:center; justify-content:space-between; gap:2rem; flex-wrap:wrap;'>
                        <div>
                            <div style='font-size: 2.8rem; font-weight: 900; color: #2563EB; margin-bottom: 0.5rem;'>{rank['badge']}</div>
                            <div class='quiz-rank-title'>{rank['title']}</div>
                            <div class='quiz-rank-subtitle'>{rank['subtitle']}</div>
                        </div>
                        <div style='text-align: center; min-width: 120px;'>
                            <div style='font-size: 3rem; font-weight: 900; color: #2563EB;'>{score}</div>
                            <div style='font-size: 1rem; color: #64748B; margin-top: 0.25rem; font-weight: 600;'>de {total}</div>
                        </div>
                    </div>
                    <div style='margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #E2E8F0; font-size: 1rem; color: #475569; line-height: 1.6;'>
                        ✨ Respondiste correctamente <strong>{score} de {total}</strong> preguntas. Continúa practicando para dominar la bioinformática.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.expander("Revisar Errores", expanded=True):
                wrong_answers = []

                for question in questions:
                    selected_key = f"question_{question['id']}"
                    selected_text = st.session_state.get(selected_key)
                    correct_option = next((opt for opt in question.get("quiz_options", []) if opt.get("is_correct")), None)
                    correct_text = correct_option["option_text"] if correct_option else "Respuesta correcta no disponible"

                    if selected_text is None or selected_text != correct_text:
                        wrong_answers.append({
                            "question": question["question"],
                            "selected": selected_text or "No respondiste esta pregunta.",
                            "correct": correct_text,
                            "explanation": question.get("explanation", "No hay explicación disponible.")
                        })

                if wrong_answers:
                    st.markdown("<div class='quiz-review-card'>", unsafe_allow_html=True)
                    st.markdown("<strong>Estos son los puntos clave para mejorar:</strong>", unsafe_allow_html=True)

                    for wrong in wrong_answers:
                        st.markdown(
                            f"""
                            <div class='quiz-review-item'>
                                <strong>{wrong['question']}</strong>
                                <div class='quiz-review-answer'>Tu respuesta: {wrong['selected']}</div>
                                <div class='quiz-review-answer'>Respuesta correcta: {wrong['correct']}</div>
                                <div class='quiz-review-answer'>Sugerencia: {wrong['explanation']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    st.markdown(
                        "<div class='quiz-review-note'>Repasa estos conceptos en los módulos de tutoriales e intenta nuevamente para subir al siguiente nivel.</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.success("¡Perfecto! No hay errores en esta ronda. Sigue así para mantener tu racha de aprendizaje.")

    except Exception as error:
        st.error("Ocurrió un error al cargar o guardar el quiz.")
        st.code(str(error))

    if st.button("Volver al inicio", type="secondary", use_container_width=True):
        st.session_state.pop("quiz_questions", None)
        st.session_state.page = "dashboard"
        st.rerun()