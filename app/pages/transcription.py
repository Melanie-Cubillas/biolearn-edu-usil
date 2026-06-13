import streamlit as st

from components.layout import load_styles, top_bar
from pages.disease_detail import DISEASE_DATA


def transcription_page():
    load_styles()
    top_bar()

    disease_key = st.session_state.get("selected_disease", "huntington")
    disease = DISEASE_DATA[disease_key]

    st.title("Transcripción")
    st.subheader(disease["title"])

    dna = st.text_input(
        "Secuencia de ADN",
        value=disease["reference_sequence"].replace(" ", "")
    )

    clean_dna = dna.replace(" ", "").upper()
    rna = clean_dna.replace("T", "U")

    st.write("**ADN:**")
    st.code(clean_dna)

    st.write("**ARNm:**")
    st.code(rna)

    st.info(
        "La transcripción convierte una secuencia de ADN en ARN mensajero. "
        "Durante este proceso, la timina se reemplaza por uracilo."
    )

    if st.button("Volver"):
        st.session_state.page = "disease_detail"
        st.rerun()
