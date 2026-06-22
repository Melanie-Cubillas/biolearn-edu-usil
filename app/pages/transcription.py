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

    # Selector de fuente visual e inhabilitado para NCBI
    st.markdown("<p style='font-size: 14.5px; font-weight: 600; color: #475569; margin-bottom: 8px;'>Fuente de la secuencia</p>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; gap: 0.75rem; align-items: center; margin-bottom: 1.5rem;">
        <div style="padding: 0.5rem 1rem; background: #3B82F6; color: white; border-radius: 8px; font-weight: 600; font-size: 14px; box-shadow: 0 4px 10px rgba(59,130,246,0.2);">Secuencia del ejemplo</div>
        <div style="padding: 0.5rem 1rem; background: #F1F5F9; color: #94A3B8; border-radius: 8px; border: 1px dashed #CBD5E1; font-size: 14px; cursor: not-allowed;">Buscar en NCBI (Disponible próximamente)</div>
    </div>
    """, unsafe_allow_html=True)

    dna = disease["reference_sequence"].replace(" ", "")
    ncbi_data = None

    dna = st.session_state.get("transcription_dna", dna)
    ncbi_data = st.session_state.get("transcription_ncbi", ncbi_data)

    dna = st.text_area("Secuencia de ADN", value=dna, height=120)

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