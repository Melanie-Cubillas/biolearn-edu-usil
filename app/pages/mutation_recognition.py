import math
import re
import html

import plotly.express as px
import streamlit as st
import pandas as pd

from components.layout import load_styles, top_bar
from pages.disease_detail import DISEASE_DATA
from services.ncbi_service import get_sequence
from services.blast_service import detect_mutations


def validate_dna_sequence(sequence: str) -> tuple[bool, str]:
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
    st.error(message)


def render_styles():
    st.html("""
    <style>
    .result-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 22px;
        padding: 1.4rem;
        box-shadow: 0 12px 28px rgba(15,23,42,.06);
        margin: 1rem 0;
    }

    .metric-card {
        background: linear-gradient(135deg, #EFF6FF, #F5F3FF);
        border: 1px solid #DBEAFE;
        border-radius: 20px;
        padding: 1.2rem;
        text-align: center;
        height: 150px;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .metric-value {
        font-size: 32px;
        font-weight: 900;
        color: #0F172A;
    }

    .metric-label {
        color: #64748B;
        font-weight: 800;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: .08em;
    }

    .section-title-custom {
        font-size: 30px;
        font-weight: 900;
        color: #0F172A;
        margin: 2rem 0 1rem 0;
    }


    .sequence-block-label {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 800;
        margin: .7rem 0 .25rem 0;
    }
   

    .base {
        width: 34px;
        height: 34px;
        border-radius: 9px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 14px;
        border: 1px solid rgba(15,23,42,.08);
    }

    .base-A { background:#DCFCE7; color:#16A34A; }
    .base-T { background:#FEE2E2; color:#DC2626; }
    .base-C { background:#DBEAFE; color:#2563EB; }
    .base-G { background:#FED7AA; color:#EA580C; }
    .base-gap { background:#F1F5F9; color:#64748B; }

    .sequence-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 1rem;
        max-height: 260px;
        overflow-y: auto;
        overflow-x: hidden;
        box-shadow: inset 0 0 0 1px rgba(226,232,240,.45);
    }

    .sequence-row {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 0;
    }

    .base-mut {
        background: linear-gradient(135deg, #8B5CF6, #A78BFA) !important;
        color: white !important;
        border: 2px solid #7C3AED !important;
        box-shadow: 0 0 10px rgba(139,92,246,.35);
    }

    .legend {
        display: flex;
        flex-wrap: wrap;
        gap: .8rem;
        color: #475569;
        font-size: 14px;
        margin-top: 1rem;
    }

    .finding-card {
        background: linear-gradient(135deg, #FEFCE8, #F5F3FF);
        border: 1px solid #E9D5FF;
        border-radius: 22px;
        padding: 1.4rem;
        margin: 1rem 0;
    }

    .step-card {
        display: flex;
        gap: .8rem;
        align-items: center;
        background: #F8FAFC;
        border: 1px solid #D8E2EF;
        border-radius: 16px;
        padding: 1rem;
        color: #334155;
        margin-bottom: .7rem;
    }

    .step-number {
        width: 34px;
        height: 34px;
        border-radius: 10px;
        background: #0B2454;
        color: white;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        flex: 0 0 auto;
    }
    </style>
    """)


def similarity_progress_ring(percent: float) -> str:
    return f"""
    <div class="metric-value">{percent:.1f}%</div>
    <div class="metric-label">Similitud</div>
    """


def mutation_summary(result):
    mutations = result["mutations"]
    return {
        "Sustitución": sum(1 for m in mutations if m["type"] == "Sustitución"),
        "Inserción": sum(1 for m in mutations if m["type"] == "Inserción"),
        "Deleción": sum(1 for m in mutations if m["type"] == "Deleción"),
    }


def render_base(base, mutated=False):
    clean = html.escape(base)

    if base == "-":
        class_name = "base base-gap"
    else:
        class_name = f"base base-{base}"

    if mutated:
        class_name += " base-mut"

    return f'<span class="{class_name}">{clean}</span>'


def render_visual_alignment(alignment):
    ref = alignment["aligned_reference"]
    qry = alignment["aligned_query"]

    ref_html = ""
    qry_html = ""

    for r, q in zip(ref, qry):
        changed = r != q
        ref_html += render_base(r, changed)
        qry_html += render_base(q, changed)

    st.html(f"""
    <div class="result-card">
        <h3 style="margin-top:0;color:#0F172A;">
            Comparación visual de secuencias
        </h3>

        <p style="color:#64748B;">
            Se muestran todas las bases. Usa el scroll dentro de cada cuadro para revisar la secuencia completa.
            Las bases moradas representan mutaciones o diferencias detectadas.
        </p>

        <div style="font-weight:900;color:#2563EB;margin-top:1rem;margin-bottom:.5rem;">
            Secuencia referencial
        </div>

        <div class="sequence-box">
            <div class="sequence-row">
                {ref_html}
            </div>
        </div>

        <div style="font-weight:900;color:#7C3AED;margin-top:1.3rem;margin-bottom:.5rem;">
            Secuencia analizada
        </div>

        <div class="sequence-box">
            <div class="sequence-row">
                {qry_html}
            </div>
        </div>

        <div class="legend">
            <span>🟩 A = Adenina</span>
            <span>🟥 T = Timina</span>
            <span>🟦 C = Citosina</span>
            <span>🟧 G = Guanina</span>
            <span>🟪 Mutación / diferencia</span>
        </div>
    </div>
    """)


def render_steps(steps):
    cards = ""

    for index, step in enumerate(steps, start=1):
        clean_step = html.escape(step.split(". ", 1)[-1])
        cards += f"""
        <div class="step-card">
            <span class="step-number">{index}</span>
            <span>{clean_step}</span>
        </div>
        """

    st.html(f"""
    <div class="result-card">
        <h3 style="color:#0F172A;margin-top:0;">Resolución paso a paso</h3>
        {cards}
    </div>
    """)


def render_finding(finding, disease_key, mutation_count):
    interpretation = finding["interpretation"].replace("🧬", "").replace("🩸", "").replace("🫁", "").strip()

    if disease_key == "huntington" and "Expansión" in interpretation:
        educational = "La expansión de CAG puede alterar la proteína huntingtina y afectar neuronas del sistema nervioso."
    elif disease_key == "anemia_falciforme" and "GAG" in interpretation:
        educational = "El cambio GAG a GTG puede modificar la hemoglobina y relacionarse con anemia falciforme."
    elif disease_key == "fibrosis_quistica" and "deleción" in interpretation.lower():
        educational = "La deleción en CFTR puede afectar el transporte de iones y alterar la función celular."
    elif mutation_count > 0:
        educational = "Se encontraron diferencias entre la secuencia referencial y la secuencia analizada."
    else:
        educational = "No se detectaron diferencias respecto a la secuencia referencial."

    st.html(f"""
    <div class="finding-card">
        <h3 style="color:#0F172A;margin-top:0;">Análisis específico de la enfermedad</h3>
        <p><b>Enfermedad:</b> {html.escape(str(finding["disease"]))}</p>
        <p><b>Patrón evaluado:</b> {html.escape(str(finding["pattern"]))}</p>
        <p><b>Valor en referencia:</b> {html.escape(str(finding["reference_value"]))}</p>
        <p><b>Valor en secuencia analizada:</b> {html.escape(str(finding["query_value"]))}</p>

        <div style="background:white;border-radius:16px;padding:1rem;margin-top:1rem;border:1px solid #E2E8F0;">
            <b>Resultado:</b> {html.escape(interpretation)}
        </div>

        <div style="background:#EFF6FF;border-radius:16px;padding:1rem;margin-top:1rem;border:1px solid #BFDBFE;color:#1E3A8A;">
            <b>Interpretación educativa:</b> {html.escape(educational)}
        </div>
    </div>
    """)


def mutation_recognition_page():
    load_styles()
    render_styles()
    top_bar()

    disease_key = st.session_state.get("selected_disease", "huntington")
    disease = DISEASE_DATA[disease_key]

    st.title("Reconocimiento de mutaciones")
    st.subheader(disease["title"])

    st.markdown(
        "<p style='font-size: 14.5px; font-weight: 600; color: #475569; margin-bottom: 8px;'>Selecciona el modo</p>",
        unsafe_allow_html=True
    )

    if "mutation_mode" not in st.session_state:
        st.session_state["mutation_mode"] = "Modo guiado"

    modo = st.radio(
        label="Selecciona el modo",
        options=["Modo guiado", "Modo exploratorio (Buscar en NCBI)"],
        index=0 if st.session_state["mutation_mode"] == "Modo guiado" else 1,
        horizontal=True,
        label_visibility="collapsed"
    )

    if modo != st.session_state["mutation_mode"]:
        st.session_state["mutation_mode"] = modo

        if modo == "Modo guiado":
            st.session_state.pop("mutation_ncbi", None)
            st.session_state["mutation_reference"] = disease["reference_sequence"].replace(" ", "")
            st.session_state["mutation_sequence"] = disease.get(
                "mutated_sequence",
                disease["reference_sequence"]
            ).replace(" ", "")

        st.rerun()

    reference = disease["reference_sequence"].replace(" ", "")
    mutated = disease.get("mutated_sequence", disease["reference_sequence"]).replace(" ", "")

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
                st.warning("Por favor, ingresa un Accession ID.")

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
        summary = mutation_summary(result)

        st.html('<div class="section-title-custom">Resultado del análisis</div>')

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.html(f"""
            <div class="metric-card">
                {similarity_progress_ring(alignment["identity_percent"])}
            </div>
            """)

        with col2:
            st.html(f"""
            <div class="metric-card">
                <div class="metric-value">{alignment["matches"]}</div>
                <div class="metric-label">Coincidencias</div>
            </div>
            """)

        with col3:
            st.html(f"""
            <div class="metric-card">
                <div class="metric-value">{alignment["mismatches"]}</div>
                <div class="metric-label">Diferencias</div>
            </div>
            """)

        with col4:
            st.html(f"""
            <div class="metric-card">
                <div class="metric-value">{alignment["gaps"]}</div>
                <div class="metric-label">Gaps</div>
            </div>
            """)

        st.html('<div class="section-title-custom">Tipos de mutaciones encontradas</div>')

        mutation_chart_data = pd.DataFrame({
            "Tipo": list(summary.keys()),
            "Cantidad": list(summary.values()),
        })

        if mutation_chart_data["Cantidad"].sum() > 0:
            mutation_fig = px.pie(
                mutation_chart_data,
                names="Tipo",
                values="Cantidad",
                hole=0.42,
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
                marker=dict(line=dict(color="#FFFFFF", width=2.5)),
            )
            mutation_fig.update_layout(
                margin=dict(l=30, r=30, t=30, b=30),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(size=13, color="#0F172A"),
            )
            st.plotly_chart(mutation_fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No se encontraron mutaciones para clasificar visualmente.")

        render_visual_alignment(alignment)

        st.html('<div class="section-title-custom">Mutaciones detectadas</div>')

        if result["mutations"]:
            df = pd.DataFrame(result["mutations"])
            df = df.rename(columns={
                "type": "Tipo",
                "position": "Posición",
                "reference_base": "Base referencial",
                "mutated_base": "Base analizada"
            })
            st.dataframe(df, use_container_width=True)
        else:
            st.success("No se detectaron mutaciones entre ambas secuencias.")

        render_finding(
            result["special_finding"],
            disease_key,
            result["mutation_count"]
        )

        render_steps(result["steps"])

        if not st.session_state.get("completed_mutation", False):
            increment = 20
            st.session_state.progress = min(100, st.session_state.get("progress", 0) + increment)
            st.session_state.completed_mutation = True

            user = st.session_state.get("user", {})
            if isinstance(user, dict) and "email" in user:
                from services.progress_service import save_user_progress
                save_user_progress(
                    user["email"],
                    st.session_state.progress,
                    st.session_state.get("streak", 1),
                    st.session_state.get("badges", 0)
                )

        if ncbi_data:
            st.html('<div class="section-title-custom">Información NCBI / FASTA</div>')
            with st.container(border=True):
                st.write(f"**ID de acceso:** {ncbi_data['id']}")
                st.write(f"**Descripción:** {ncbi_data['description']}")
                st.write(f"**Fuente de datos:** {ncbi_data['source']}")
                if "length" in ncbi_data:
                    st.write(f"**Longitud de la secuencia:** {ncbi_data['length']} pb")

    if st.button("Volver", type="secondary", use_container_width=True):
        st.session_state.page = "disease_detail"
        st.rerun()