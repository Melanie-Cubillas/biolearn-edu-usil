import streamlit as st
from components.layout import load_styles, top_bar


DISEASE_DATA = {
    "huntington": {
        "title": "Enfermedad de Huntington",
        "gene": "HTT",
        "accession_id": "NM_002111",
        "mutation_pattern": "CAG",
        "concept": "Trastorno neurodegenerativo hereditario asociado a una expansión de repeticiones CAG en el gen HTT.",
        "symptoms": "Movimientos involuntarios, deterioro cognitivo y alteraciones conductuales.",
        "causes": "Expansión anormal del triplete CAG.",
        "reference_sequence": "CAGCAGCAGCAGCAG",
        "mutated_sequence": "CAGCAGCAGCAGCAGCAGCAGCAG"
    },
    "anemia_falciforme": {
        "title": "Anemia falciforme",
        "gene": "HBB",
        "accession_id": "NM_000518",
        "mutation_pattern": "GAG>GTG",
        "concept": "Enfermedad hereditaria causada por una alteración en el gen HBB, que modifica la hemoglobina.",
        "symptoms": "Fatiga, dolor, anemia, infecciones frecuentes y problemas circulatorios.",
        "causes": "Mutación puntual en el gen HBB. El codón GAG puede cambiar a GTG, alterando el aminoácido producido.",
        "reference_sequence": "ATGGTGCACCTGACTCCTGAGGAGAAGTCT",
        "mutated_sequence": "ATGGTGCACCTGACTCCTGTGGAGAAGTCT"
    },
    "fibrosis_quistica": {
        "title": "Fibrosis quística",
        "gene": "CFTR",
        "accession_id": "NM_000492",
        "mutation_pattern": "Deleción F508",
        "concept": "Enfermedad genética que afecta principalmente pulmones y sistema digestivo por alteraciones en el gen CFTR.",
        "symptoms": "Tos persistente, infecciones respiratorias, mucosidad espesa y problemas digestivos.",
        "causes": "Mutaciones en el gen CFTR. Una de las más conocidas es la deleción F508.",
        "reference_sequence": "ATCATCTTTGGTGTTTCCTATGATGAATATAG",
        "mutated_sequence": "ATCATCGGTGTTTCCTATGATGAATATAG"
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
