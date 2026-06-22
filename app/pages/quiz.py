import random
import streamlit as st

from components.layout import load_styles, top_bar
from services.supabase_service import (
    is_supabase_configured,
    get_quiz_questions,
    save_quiz_result
)


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

            selected_label = st.radio(
                "Selecciona una respuesta",
                list(option_map.keys()),
                index=saved_idx,
                disabled=st.session_state.quiz_submitted,
                key=f"question_{question['id']}"
            )

            if selected_label is None:
                unanswered_questions.append(index + 1)
            else:
                selected_answers[question["id"]] = option_map[selected_label]

            if st.session_state.quiz_submitted:
                user_opt = option_map.get(selected_label)
                if user_opt:
                    if user_opt["is_correct"]:
                        st.success("Respuesta correcta")
                    else:
                        st.error("Respuesta incorrecta")
                        correct_opt = next((o for o in options if o["is_correct"]), None)
                        if correct_opt:
                            st.info(f"Respuesta correcta: {correct_opt['option_text']}")
                else:
                    st.warning("No respondiste esta pregunta.")

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
                    new_progress = max(st.session_state.get("progress", 0), 80)
                    st.session_state.progress = new_progress

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

            if score == total:
                st.success("Excelente. Dominas los conceptos evaluados de bioinformática.")
            elif score >= total / 2:
                st.info("Buen avance. Revisa los temas donde tuviste dudas.")
            else:
                st.warning("Te recomendamos revisar los tutoriales antes de volver a intentarlo.")

    except Exception as error:
        st.error("Ocurrió un error al cargar o guardar el quiz.")
        st.code(str(error))

    if st.button("Volver al inicio", type="secondary", use_container_width=True):
        st.session_state.pop("quiz_questions", None)
        st.session_state.page = "dashboard"
        st.rerun()