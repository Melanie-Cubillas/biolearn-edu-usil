import math
import re

import plotly.express as px
import streamlit as st
import pandas as pd

from components.layout import load_styles, top_bar
from pages.disease_detail import DISEASE_DATA
from services.ncbi_service import get_sequence
from services.blast_service import detect_mutations


def validate_dna_sequence(sequence: str) -> tuple[bool, str]:
    """Validate DNA sequence (ATCG only, case-insensitive)."""
    seq_clean = sequence.strip().upper().replace(" ", "").replace("\n", "")
    if not seq_clean:
        return False, "Por favor, ingresa una secuencia."
    if not re.match(r"^[ATCG]+$", seq_clean):
        invalid_chars = set(seq_clean) - set("ATCG")
        return False, f"La secuencia contiene caracteres inválidos: {', '.join(sorted(invalid_chars))}. Solo se permiten A, T, C, G."
    if len(seq_clean) < 5:
        return False, "La secuencia debe tener al menos 5 bases nitrogenadas."
    return True, seq_clean


def render_validation_error(message: str):
    """Render custom validation error card."""
    st.markdown(f"""
    <div style='border: 1px solid #FECACA; background: #FEF2F2; border-radius: 14px; padding: 1rem; margin: 1rem 0;'>
        <div style='color: #991B1B; font-weight: 700; margin-bottom: 0.5rem;'>Validación requerida</div>
        <div style='color: #7F1D1D; font-size: 0.95rem;'>{message}</div>
    </div>
    """, unsafe_allow_html=True)


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
        ref_valid, ref_msg = validate_dna_sequence(reference)
        mut_valid, mut_msg = validate_dna_sequence(mutated)
        
        if not ref_valid:
            render_validation_error(f"Secuencia referencial: {ref_msg}")
            st.stop()
        if not mut_valid:
            render_validation_error(f"Secuencia analizada: {mut_msg}")
            st.stop()
        
        reference = ref_msg
        mutated = mut_msg
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
                textfont_size=12,
                textposition="outside",
                marker=dict(line=dict(color="#FFFFFF", width=2.5)),
            )
            mutation_fig.update_layout(
                margin=dict(l=40, r=40, t=40, b=80),
                legend=dict(orientation="h", y=-0.22, x=0.5, xanchor="center", font=dict(size=12, family="Outfit, sans-serif")),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Outfit, sans-serif", size=12, color="#0F172A"),
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