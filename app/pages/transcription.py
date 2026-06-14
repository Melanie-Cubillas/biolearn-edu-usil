import streamlit as st

from components.layout import load_styles, top_bar
from pages.disease_detail import DISEASE_DATA
from services.ncbi_service import get_sequence
from services.bioinformatics_service import transcribe_dna_to_rna, find_stop_codons


def transcription_page():
    load_styles()
    top_bar()

    disease_key = st.session_state.get("selected_disease", "huntington")
    disease = DISEASE_DATA[disease_key]

    st.title("Transcripción")
    st.subheader(disease["title"])

    source = st.radio(
        "Fuente de la secuencia",
        ["Secuencia del ejemplo", "Buscar en NCBI"],
        horizontal=True
    )

    dna = disease["reference_sequence"].replace(" ", "")
    ncbi_data = None

    if source == "Buscar en NCBI":
        accession_id = st.text_input("Accession ID", value="NM_002111")

        if st.button("Obtener secuencia desde NCBI"):
            ncbi_data = get_sequence(accession_id)
            dna = ncbi_data["sequence"]
            st.session_state["transcription_dna"] = dna
            st.session_state["transcription_ncbi"] = ncbi_data

    dna = st.session_state.get("transcription_dna", dna)
    ncbi_data = st.session_state.get("transcription_ncbi", ncbi_data)

    dna = st.text_area("Secuencia de ADN", value=dna, height=120)

    if st.button("Transcribir ADN a ARN"):
        result = transcribe_dna_to_rna(dna)
        stop_codons = find_stop_codons(result["rna"])

        st.subheader("Resultado")

        st.write("ADN limpio:")
        st.code(result["dna"])

        st.write("ARN mensajero:")
        st.code(result["rna"])

        st.subheader("¿Cómo se solucionó?")
        for step in result["steps"]:
            st.write(step)

        st.subheader("Codones de parada encontrados")
        if stop_codons:
            st.dataframe(stop_codons, use_container_width=True)
        else:
            st.info("No se encontró codón de parada UAA, UAG o UGA.")

        if ncbi_data:
            st.subheader("Información NCBI / FASTA")
            st.write(f"ID: {ncbi_data['id']}")
            st.write(f"Descripción: {ncbi_data['description']}")
            st.write(f"Fuente: {ncbi_data['source']}")
            st.write(f"Archivo local: {ncbi_data['file_path']}")

            st.subheader("Pasos de lectura/escritura FASTA")
            for step in ncbi_data["steps"]:
                st.write(step)

    if st.button("Volver"):
        st.session_state.page = "disease_detail"
        st.rerun()