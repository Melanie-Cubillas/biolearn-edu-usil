import streamlit as st
from components.layout import load_styles, top_bar


DISEASE_DATA = {
    "huntington": {
        "title": "Enfermedad de Huntington",
        "concept": "La enfermedad de Huntington es un trastorno neurodegenerativo hereditario asociado a una expansión de repeticiones CAG en el gen HTT.",
        "symptoms": "Puede causar alteraciones motoras, cognitivas y conductuales.",
        "causes": "Su causa principal es una mutación por expansión de tripletes CAG.",
        "reference_sequence": "CAG CAG CAG CAG CAG",
        "mutated_sequence": "CAG CAG CAG CAG CAG CAG CAG CAG CAG"
    },
    "anemia_falciforme": {
        "title": "Anemia falciforme",
        "concept": "La anemia falciforme es una enfermedad hereditaria que altera la estructura de la hemoglobina.",
        "symptoms": "Puede causar fatiga, dolor, infecciones frecuentes y problemas circulatorios.",
        "causes": "Se produce por una mutación puntual en el gen HBB.",
        "reference_sequence": "GAG",
        "mutated_sequence": "GTG"
    },
    "fibrosis_quistica": {
        "title": "Fibrosis quística",
        "concept": "La fibrosis quística es una enfermedad genética que afecta principalmente pulmones y sistema digestivo.",
        "symptoms": "Puede causar tos persistente, infecciones respiratorias y problemas digestivos.",
        "causes": "Está asociada a mutaciones en el gen CFTR.",
        "reference_sequence": "ATC TTT GGT",
        "mutated_sequence": "ATC GGT"
    }
}


def disease_detail_page():
    load_styles()
    top_bar()

    disease_key = st.session_state.get("selected_disease", "huntington")
    disease = DISEASE_DATA[disease_key]

    st.title(disease["title"])

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.subheader("Concepto médico y nivel genético")
            st.write(disease["concept"])

    with col2:
        with st.container(border=True):
            st.subheader("Síntomas")
            st.write(disease["symptoms"])

    with col3:
        with st.container(border=True):
            st.subheader("Causas")
            st.write(disease["causes"])

    st.subheader("Impacto")

    impact1, impact2, impact3 = st.columns(3)

    with impact1:
        st.info("Gráfico de lugares con mayores casos en los últimos años.")

    with impact2:
        st.info("Gráfico etario en los últimos años.")

    with impact3:
        st.info("Gráfico por género en los últimos años.")

    st.subheader("Secuencias")

    st.text_input(
        "Secuencia referencial",
        value=disease["reference_sequence"],
        disabled=True
    )

    st.text_input(
        "Secuencia mutada",
        value=disease["mutated_sequence"],
        disabled=True
    )

    st.subheader("¿Qué te gustaría realizar?")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        if st.button("Traducción", use_container_width=True):
            st.session_state.page = "translation"
            st.rerun()

    with col_b:
        if st.button("Transcripción", use_container_width=True):
            st.session_state.page = "transcription"
            st.rerun()

    with col_c:
        if st.button("Reconocer mutaciones", use_container_width=True):
            st.session_state.page = "mutation_recognition"
            st.rerun()

    if st.button("Volver a enfermedades"):
        st.session_state.page = "diseases"
        st.rerun()
