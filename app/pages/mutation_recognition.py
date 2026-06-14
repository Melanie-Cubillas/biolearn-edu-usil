import streamlit as st
import pandas as pd

from components.layout import load_styles, top_bar
from pages.disease_detail import DISEASE_DATA
from services.ncbi_service import get_sequence
from services.blast_service import detect_mutations


def mutation_recognition_page():
    load_styles()
    top_bar()

    disease_key = st.session_state.get("selected_disease", "huntington")
    disease = DISEASE_DATA[disease_key]

    st.title("Reconocimiento de mutaciones")
    st.subheader(disease["title"])

    reference = disease["reference_sequence"].replace(" ", "")
    mutated = disease["mutated_sequence"].replace(" ", "")

    mode = st.radio(
        "Selecciona el modo",
        ["Modo guiado", "Modo exploratorio"],
        horizontal=True
    )

    ncbi_data = None

    if mode == "Modo exploratorio":
        st.info("En este modo puedes obtener una secuencia real desde NCBI y guardarla como FASTA local.")

        accession_id = st.text_input("Accession ID", value="NM_002111")

        if st.button("Buscar en NCBI"):
            ncbi_data = get_sequence(accession_id)
            st.session_state["mutation_ncbi"] = ncbi_data
            st.session_state["mutation_sequence"] = ncbi_data["sequence"]

    ncbi_data = st.session_state.get("mutation_ncbi", ncbi_data)

    if "mutation_sequence" in st.session_state:
        mutated = st.session_state["mutation_sequence"]

    reference = st.text_area("Secuencia referencial", value=reference, height=100)
    mutated = st.text_area("Secuencia mutada / analizada", value=mutated, height=100)

    if st.button("Reconocer mutaciones"):
        result = detect_mutations(reference, mutated, disease_key=disease_key)
        alignment = result["alignment"]

        st.subheader("Estadísticas del alineamiento")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Identidad", f"{alignment['identity_percent']}%")
        col2.metric("Coincidencias", alignment["matches"])
        col3.metric("Diferencias", alignment["mismatches"])
        col4.metric("Gaps", alignment["gaps"])

        st.subheader("Comparación tipo BLAST educativo")

        st.write("Secuencia referencial alineada:")
        st.code(alignment["aligned_reference"])

        st.write("Coincidencias y diferencias:")
        st.code(alignment["match_line"])

        st.write("Secuencia mutada alineada:")
        st.code(alignment["aligned_query"])

        st.subheader("Mutaciones detectadas")

        if result["mutations"]:
            df = pd.DataFrame(result["mutations"])
            st.dataframe(df, use_container_width=True)
        else:
            st.success("No se detectaron mutaciones entre ambas secuencias.")

        st.subheader("Análisis específico de la enfermedad")

        finding = result["special_finding"]

        st.write(f"Enfermedad: {finding['disease']}")
        st.write(f"Patrón evaluado: {finding['pattern']}")
        st.write(f"Valor en referencia: {finding['reference_value']}")
        st.write(f"Valor en secuencia analizada: {finding['query_value']}")
        st.warning(finding["interpretation"])

        st.subheader("Interpretación educativa")

        if disease_key == "huntington" and "Expansión" in finding["interpretation"]:
            st.write("La expansión de CAG puede alterar la proteína huntingtina.")

        elif disease_key == "anemia_falciforme" and "GAG → GTG" in finding["interpretation"]:
            st.write("El cambio GAG → GTG puede modificar la hemoglobina y relacionarse con anemia falciforme.")

        elif disease_key == "fibrosis_quistica" and "deleción" in finding["interpretation"].lower():
            st.write("La deleción en CFTR puede afectar el transporte de iones y alterar la función celular.")

        elif result["mutation_count"] > 0:
            st.write("Se encontraron diferencias entre la secuencia referencial y la secuencia analizada.")
        else:
            st.write("No se detectaron diferencias respecto a la secuencia referencial.")
                
        st.subheader("¿Cómo se solucionó?")
        for step in result["steps"]:
            st.write(step)

        if ncbi_data:
            st.subheader("Información NCBI / FASTA")
            st.write(f"ID: {ncbi_data['id']}")
            st.write(f"Descripción: {ncbi_data['description']}")
            st.write(f"Longitud: {ncbi_data['length']}")
            st.write(f"Fuente: {ncbi_data['source']}")
            st.write(f"Archivo local: {ncbi_data['file_path']}")

            st.subheader("Pasos de lectura/escritura FASTA")
            for step in ncbi_data["steps"]:
                st.write(step)

    if st.button("Volver"):
        st.session_state.page = "disease_detail"
        st.rerun()