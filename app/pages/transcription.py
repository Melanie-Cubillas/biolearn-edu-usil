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

    st.title("Transcripción de ADN")
    st.subheader(disease["title"])

    # Selector de fuente interactivo
    st.markdown("<p style='font-size: 14.5px; font-weight: 600; color: #475569; margin-bottom: 8px;'>Fuente de la secuencia</p>", unsafe_allow_html=True)
    
    if "transcription_source" not in st.session_state:
        st.session_state["transcription_source"] = "Secuencia del ejemplo"

    fuente_seq = st.radio(
        label="Fuente de la secuencia",
        options=["Secuencia del ejemplo", "Buscar en NCBI (Exploratorio)"],
        index=0 if st.session_state["transcription_source"] == "Secuencia del ejemplo" else 1,
        horizontal=True,
        label_visibility="collapsed"
    )

    # Manejar cambio de fuente
    if fuente_seq != st.session_state["transcription_source"]:
        st.session_state["transcription_source"] = fuente_seq
        if fuente_seq == "Secuencia del ejemplo":
            if "transcription_ncbi" in st.session_state:
                del st.session_state["transcription_ncbi"]
            st.session_state["transcription_dna"] = disease["reference_sequence"].replace(" ", "")
        st.rerun()

    dna = disease["reference_sequence"].replace(" ", "")
    ncbi_data = None

    dna = st.session_state.get("transcription_dna", dna)
    ncbi_data = st.session_state.get("transcription_ncbi", ncbi_data)

    if fuente_seq == "Buscar en NCBI (Exploratorio)":
        col_input, col_btn = st.columns([3, 1])
        with col_input:
            acc_id = st.text_input(
                "Accession ID de NCBI",
                value=disease.get("accession_id", ""),
                key="transcription_acc_id_input",
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
                        st.session_state["transcription_dna"] = res["sequence"]
                        st.session_state["transcription_ncbi"] = res
                        st.success(f"Secuencia obtenida: {res['description'][:60]}...")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al conectar con NCBI: {str(e)}")
            else:
                st.warning("Por favor, ingrese un Accession ID.")

    dna = st.text_area("Secuencia de ADN", value=dna, height=120)
    st.session_state["transcription_dna"] = dna

    if st.button("Transcribir ADN a ARN", type="primary"):
        result = transcribe_dna_to_rna(dna)
        stop_codons = find_stop_codons(result["rna"])

        st.subheader("Resultado")

        st.write("ADN limpio:")
        st.code(result["dna"])

        st.write("ARN mensajero:")
        st.code(result["rna"])

        st.subheader("Resolución paso a paso")
        for step in result["steps"]:
            st.write(step)

        st.subheader("Codones de parada encontrados")
        if stop_codons:
            st.dataframe(stop_codons, use_container_width=True)
        else:
            st.info("No se encontró codón de parada UAA, UAG o UGA.")

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