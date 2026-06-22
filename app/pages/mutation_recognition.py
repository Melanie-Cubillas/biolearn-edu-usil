import math

import plotly.express as px
import streamlit as st
import pandas as pd

from components.layout import load_styles, top_bar
from pages.disease_detail import DISEASE_DATA
from services.ncbi_service import get_sequence
from services.blast_service import detect_mutations


def similarity_progress_ring(percent: float) -> str:
    radius = 56
    circumference = 2 * math.pi * radius
    dash_offset = circumference * (1 - min(max(percent, 0), 100) / 100)

    return f"""
    <div class="progress-ring">
        <svg width="140" height="140" viewBox="0 0 140 140">
            <circle class="progress-ring-bg" cx="70" cy="70" r="{radius}" />
            <circle class="progress-ring-progress" cx="70" cy="70" r="{radius}"
                stroke-dasharray="{circumference:.2f} {circumference:.2f}"
                stroke-dashoffset="{dash_offset:.2f}" />
        </svg>
        <div class="progress-ring-text">
            <div style="font-size: 2rem;">{percent:.1f}%</div>
            <span>Similitud</span>
        </div>
    </div>
    """


def mutation_recognition_page():
    load_styles()
    top_bar()

    disease_key = st.session_state.get("selected_disease", "huntington")
    disease = DISEASE_DATA[disease_key]

    st.title("Reconocimiento de mutaciones")
    st.subheader(disease["title"])

    reference = disease["reference_sequence"].replace(" ", "")
    mutated = disease["mutated_sequence"].replace(" ", "")

    # Selector de modo visual e inhabilitado para Exploratorio
    st.markdown("<p style='font-size: 14.5px; font-weight: 600; color: #475569; margin-bottom: 8px;'>Selecciona el modo</p>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; gap: 0.75rem; align-items: center; margin-bottom: 1.5rem;">
        <div style="padding: 0.5rem 1rem; background: #3B82F6; color: white; border-radius: 8px; font-weight: 600; font-size: 14px; box-shadow: 0 4px 10px rgba(59,130,246,0.2);">Modo guiado</div>
        <div style="padding: 0.5rem 1rem; background: #F1F5F9; color: #94A3B8; border-radius: 8px; border: 1px dashed #CBD5E1; font-size: 14px; cursor: not-allowed;">Modo exploratorio (Disponible próximamente)</div>
    </div>
    """, unsafe_allow_html=True)

    ncbi_data = None
    ncbi_data = st.session_state.get("mutation_ncbi", ncbi_data)

    if "mutation_sequence" in st.session_state:
        mutated = st.session_state["mutation_sequence"]

    reference = st.text_area("Secuencia referencial", value=reference, height=100)
    mutated = st.text_area("Secuencia mutada / analizada", value=mutated, height=100)

    if st.button("Reconocer mutaciones", type="primary"):
        result = detect_mutations(reference, mutated, disease_key=disease_key)
        alignment = result["alignment"]

        st.subheader("Estadísticas del alineamiento")

        col1, col2, col3, col4 = st.columns(4)

        col1.markdown(similarity_progress_ring(alignment["identity_percent"]), unsafe_allow_html=True)
        col2.metric("Coincidencias", alignment["matches"])
        col3.metric("Diferencias", alignment["mismatches"])
        col4.metric("Gaps", alignment["gaps"])

        st.subheader("Distribución de tipos de mutaciones")

        mutation_type_counts = {
            "Sustitución": sum(1 for mutation in result["mutations"] if mutation["type"] == "Sustitución"),
            "Inserción": sum(1 for mutation in result["mutations"] if mutation["type"] == "Inserción"),
            "Deleción": sum(1 for mutation in result["mutations"] if mutation["type"] == "Deleción"),
        }

        mutation_chart_data = pd.DataFrame({
            "Tipo": list(mutation_type_counts.keys()),
            "Cantidad": list(mutation_type_counts.values()),
        })

        if mutation_chart_data["Cantidad"].sum() > 0:
            mutation_fig = px.pie(
                mutation_chart_data,
                names="Tipo",
                values="Cantidad",
                hole=0.38,
                color="Tipo",
                color_discrete_map={
                    "Sustitución": "#2563EB",
                    "Inserción": "#10B981",
                    "Deleción": "#EF4444",
                },
            )
            mutation_fig.update_traces(
                textinfo="percent+label",
                textfont_size=13,
                marker=dict(line=dict(color="#FFFFFF", width=2)),
            )
            mutation_fig.update_layout(
                margin=dict(l=0, r=0, t=20, b=0),
                legend=dict(orientation="h", y=-0.16),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(mutation_fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No se encontraron mutaciones para clasificar visualmente.")

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