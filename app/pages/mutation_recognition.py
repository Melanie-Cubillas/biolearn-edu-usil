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

    # Selector de modo interactivo
    st.markdown("<p style='font-size: 14.5px; font-weight: 600; color: #475569; margin-bottom: 8px;'>Selecciona el modo</p>", unsafe_allow_html=True)
    
    if "mutation_mode" not in st.session_state:
        st.session_state["mutation_mode"] = "Modo guiado"

    modo = st.radio(
        label="Selecciona el modo",
        options=["Modo guiado", "Modo exploratorio (Buscar en NCBI)"],
        index=0 if st.session_state["mutation_mode"] == "Modo guiado" else 1,
        horizontal=True,
        label_visibility="collapsed"
    )

    # Manejar cambio de modo
    if modo != st.session_state["mutation_mode"]:
        st.session_state["mutation_mode"] = modo
        if modo == "Modo guiado":
            if "mutation_ncbi" in st.session_state:
                del st.session_state["mutation_ncbi"]
            st.session_state["mutation_reference"] = disease["reference_sequence"].replace(" ", "")
            st.session_state["mutation_sequence"] = disease["mutated_sequence"].replace(" ", "")
        st.rerun()

    reference = disease["reference_sequence"].replace(" ", "")
    mutated = disease["mutated_sequence"].replace(" ", "")

    reference = st.session_state.get("mutation_reference", reference)
    mutated = st.session_state.get("mutation_sequence", mutated)
    ncbi_data = st.session_state.get("mutation_ncbi", None)

    if modo == "Modo exploratorio (Buscar en NCBI)":
        col_input, col_btn = st.columns([3, 1])
        with col_input:
            acc_id = st.text_input(
                "Accession ID de NCBI para la referencia",
                value=disease.get("accession_id", ""),
                key="mutation_acc_id_input",
                placeholder="Ej. NM_002111"
            )
        with col_btn:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            buscar_clicked = st.button("Buscar en NCBI", type="secondary", use_container_width=True)

        if buscar_clicked:
            if acc_id:
                with st.spinner("Buscando secuencia en NCBI..."):
                    try:
                        res = get_sequence(acc_id, db="nucleotide")
                        st.session_state["mutation_reference"] = res["sequence"]
                        st.session_state["mutation_ncbi"] = res
                        st.success(f"Secuencia de referencia obtenida: {res['description'][:60]}...")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al conectar con NCBI: {str(e)}")
            else:
                st.warning("Por favor, ingrese un Accession ID.")

    reference = st.text_area("Secuencia referencial", value=reference, height=100)
    st.session_state["mutation_reference"] = reference

    mutated = st.text_area("Secuencia mutada / analizada", value=mutated, height=100)
    st.session_state["mutation_sequence"] = mutated

    if st.button("Reconocer mutaciones", type="primary"):
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
        
        # Eliminar emojis de la interpretación si existen
        interpretation_clean = finding["interpretation"].replace("🧬", "").replace("🩸", "").replace("🫁", "").strip()
        st.warning(interpretation_clean)

        st.subheader("Interpretación educativa")

        if disease_key == "huntington" and "Expansión" in finding["interpretation"]:
            st.write("La expansión de CAG puede alterar la proteína huntingtina.")

        elif disease_key == "anemia_falciforme" and "GAG" in finding["interpretation"]:
            st.write("El cambio GAG a GTG puede modificar la hemoglobina y relacionarse con anemia falciforme.")

        elif disease_key == "fibrosis_quistica" and "deleción" in finding["interpretation"].lower():
            st.write("La deleción en CFTR puede afectar el transporte de iones y alterar la función celular.")

        elif result["mutation_count"] > 0:
            st.write("Se encontraron diferencias entre la secuencia referencial y la secuencia analizada.")
        else:
            st.write("No se detectaron diferencias respecto a la secuencia referencial.")
                
        st.subheader("Resolución paso a paso")
        for step in result["steps"]:
            st.write(step)

        if ncbi_data:
            st.subheader("Información NCBI / FASTA")
            st.write(f"ID de acceso: {ncbi_data['id']}")
            st.write(f"Descripción: {ncbi_data['description']}")
            st.write(f"Fuente de datos: {ncbi_data['source']}")
            if "length" in ncbi_data:
                st.write(f"Longitud de la secuencia: {ncbi_data['length']} pb")

    if st.button("Volver", type="secondary", use_container_width=True):
        st.session_state.page = "disease_detail"
        st.rerun()