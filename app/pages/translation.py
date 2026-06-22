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

    st.title("Traducción de Proteínas")
    st.subheader(disease["title"])

    # Selector de fuente visual e inhabilitado para NCBI
    st.markdown("<p style='font-size: 14.5px; font-weight: 600; color: #475569; margin-bottom: 8px;'>Fuente de la secuencia</p>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; gap: 0.75rem; align-items: center; margin-bottom: 1.5rem;">
        <div style="padding: 0.5rem 1rem; background: #3B82F6; color: white; border-radius: 8px; font-weight: 600; font-size: 14px; box-shadow: 0 4px 10px rgba(59,130,246,0.2);">Secuencia del ejemplo</div>
        <div style="padding: 0.5rem 1rem; background: #F1F5F9; color: #94A3B8; border-radius: 8px; border: 1px dashed #CBD5E1; font-size: 14px; cursor: not-allowed;">Buscar en NCBI (Disponible próximamente)</div>
    </div>
    """, unsafe_allow_html=True)

    dna = disease["mutated_sequence"].replace(" ", "")
    ncbi_data = None

    dna = st.session_state.get("translation_dna", dna)
    ncbi_data = st.session_state.get("translation_ncbi", ncbi_data)

    dna = st.text_area("Secuencia de ADN", value=dna, height=120)

    if st.button("Traducir ADN a proteína", type="primary"):
        result = translate_dna_to_protein(dna)

        st.subheader("Resultado")

        st.write("ARN generado:")
        st.code(result["rna"])

        st.write("Codones del ARN:")
        st.code(" | ".join(result["codons"][:80]))

        st.write("Proteína resultante:")
        st.code(result["protein"])

        st.subheader("Conversión codón a aminoácido")
        df = pd.DataFrame(result["codon_table"])
        st.dataframe(df, use_container_width=True)

        st.subheader("Codones de parada")
        if result["stop_codons"]:
            st.dataframe(result["stop_codons"], use_container_width=True)
        else:
            st.info("No se encontró codón de parada en el fragmento analizado.")

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