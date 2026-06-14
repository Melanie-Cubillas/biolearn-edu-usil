import streamlit as st
import pandas as pd

from components.layout import load_styles, top_bar
from pages.disease_detail import DISEASE_DATA
from services.ncbi_service import get_sequence
from services.bioinformatics_service import translate_dna_to_protein


def translation_page():
    load_styles()
    top_bar()

    disease_key = st.session_state.get("selected_disease", "huntington")
    disease = DISEASE_DATA[disease_key]

    st.title("Traducción")
    st.subheader(disease["title"])

    source = st.radio(
        "Fuente de la secuencia",
        ["Secuencia del ejemplo", "Buscar en NCBI"],
        horizontal=True
    )

    dna = disease["mutated_sequence"].replace(" ", "")
    ncbi_data = None

    if source == "Buscar en NCBI":
        accession_id = st.text_input("Accession ID", value="NM_002111")

        if st.button("Obtener secuencia desde NCBI"):
            ncbi_data = get_sequence(accession_id)
            dna = ncbi_data["sequence"]
            st.session_state["translation_dna"] = dna
            st.session_state["translation_ncbi"] = ncbi_data

    dna = st.session_state.get("translation_dna", dna)
    ncbi_data = st.session_state.get("translation_ncbi", ncbi_data)

    dna = st.text_area("Secuencia de ADN", value=dna, height=120)

    if st.button("Traducir ADN a proteína"):
        result = translate_dna_to_protein(dna)

        st.subheader("Resultado")

        st.write("ARN generado:")
        st.code(result["rna"])

        st.write("Codones del ARN:")
        st.code(" | ".join(result["codons"][:80]))

        st.write("Proteína resultante:")
        st.code(result["protein"])

        st.subheader("Conversión codón → aminoácido")
        df = pd.DataFrame(result["codon_table"])
        st.dataframe(df, use_container_width=True)

        st.subheader("Codones de parada")
        if result["stop_codons"]:
            st.dataframe(result["stop_codons"], use_container_width=True)
        else:
            st.info("No se encontró codón de parada en el fragmento analizado.")

        st.subheader("¿Cómo se solucionó?")
        for step in result["steps"]:
            st.write(step)

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