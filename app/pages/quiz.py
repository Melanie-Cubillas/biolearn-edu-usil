import streamlit as st
from components.layout import load_styles, top_bar


QUESTIONS = [
    {
        "question": "¿Qué molécula almacena la información genética?",
        "options": ["ARN", "ADN", "Proteína", "Glucosa"],
        "answer": "ADN"
    },
    {
        "question": "¿Qué base del ADN se reemplaza por uracilo en el ARN?",
        "options": ["Adenina", "Timina", "Citosina", "Guanina"],
        "answer": "Timina"
    },
    {
        "question": "¿Qué representa un codón?",
        "options": [
            "Un grupo de tres nucleótidos",
            "Una proteína completa",
            "Una célula",
            "Una enfermedad"
        ],
        "answer": "Un grupo de tres nucleótidos"
    }
]


def quiz_page():
    load_styles()
    top_bar()

    st.title("Pon a prueba tus conocimientos")

    answers = []

    for index, item in enumerate(QUESTIONS):
        st.subheader(f"Pregunta {index + 1}")
        response = st.radio(
            item["question"],
            item["options"],
            key=f"question_{index}"
        )
        answers.append(response)

    if st.button("Enviar respuestas"):
        score = 0

        for index, item in enumerate(QUESTIONS):
            if answers[index] == item["answer"]:
                score += 1

        st.success(f"Tu puntaje es {score}/{len(QUESTIONS)}")

        if score == len(QUESTIONS):
            st.balloons()
            st.write("Excelente. Dominas los conceptos básicos.")
        elif score >= 2:
            st.info("Buen avance. Revisa los temas donde tuviste dudas.")
        else:
            st.warning("Te recomendamos revisar los tutoriales antes de intentarlo nuevamente.")

    if st.button("Volver al inicio"):
        st.session_state.page = "dashboard"
        st.rerun()