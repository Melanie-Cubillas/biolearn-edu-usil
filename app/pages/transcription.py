import html
import re

import streamlit as st

from components.layout import load_styles, top_bar
from pages.disease_detail import DISEASE_DATA
from services.ncbi_service import get_sequence
from services.bioinformatics_service import transcribe_dna_to_rna, find_stop_codons


def validate_dna_sequence(sequence: str) -> tuple[bool, str]:
    seq_clean = sequence.strip().upper().replace(" ", "").replace("\n", "")
    if not seq_clean:
        return False, "Por favor, ingresa una secuencia de ADN."
    if not re.match(r"^[ATCG]+$", seq_clean):
        invalid_chars = set(seq_clean) - set("ATCG")
        return False, f"Caracteres inválidos detectados: {', '.join(sorted(invalid_chars))}. Solo permite A, T, C, G."
    if len(seq_clean) < 5:
        return False, "La secuencia debe tener al menos 5 bases."
    return True, seq_clean


def render_validation_error(message: str):
    st.error(message)


def _sequence_tokens(sequence, limit=180):
    sequence = (sequence or "")[:limit]
    return "".join(
        f"<span class='bio-token'>{html.escape(base)}</span>"
        for base in sequence
    )


def _step_cards(steps):
    return "".join(
        f"""
        <div class="bio-step">
            <span class="bio-step-index">{index}</span>
            <span>{html.escape(step.split(". ", 1)[-1])}</span>
        </div>
        """
        for index, step in enumerate(steps, start=1)
    )


def _stop_codon_cards(stop_codons):
    if not stop_codons:
        return """
        <div class="bio-empty-state">
            No se encontró codón de parada en el fragmento analizado.
        </div>
        """

    return "".join(
        f"""
        <div class="stop-card">
            <div class="stop-codon">{html.escape(item["codon"])}</div>
            <div>Codón #{item["codon_position"]}</div>
            <small>Base inicial: {item["base_position"]}</small>
        </div>
        """
        for item in stop_codons
    )


def render_transcription_styles():
    st.html("""
    <style>
    .bio-flow-panel {
        background: #FFFFFF;
        border: 1px solid #D8E2EF;
        border-radius: 18px;
        padding: 1.4rem;
        margin: 1.25rem 0;
        box-shadow: 0 14px 32px rgba(15, 23, 42, 0.07);
    }

    .bio-flow-title {
        color: #061A3A;
        font-size: 24px;
        font-weight: 900;
        margin-bottom: 1.2rem;
    }

    .bio-flow {
        display: grid;
        grid-template-columns: minmax(0, 1fr) 64px minmax(0, 1fr);
        gap: 1.2rem;
        align-items: center;
    }

    .bio-node {
        min-height: 210px;
        border-radius: 18px;
        border: 1px solid #BFDBFE;
        background: linear-gradient(180deg, #F8FAFC 0%, #EFF6FF 100%);
        padding: 1.2rem;
        overflow: hidden;
    }

    .bio-node-rna {
        border-color: #C4B5FD;
        background: linear-gradient(180deg, #F8FAFC 0%, #F5F3FF 100%);
    }

    .bio-node-label {
        color: #2563EB;
        font-size: 14px;
        font-weight: 900;
        letter-spacing: .14em;
        text-transform: uppercase;
        margin-bottom: .9rem;
    }

    .bio-token-wrap {
        display: flex;
        flex-wrap: wrap;
        gap: .55rem;
        max-height: 145px;
        overflow: auto;
        padding-right: .25rem;
    }

    .bio-token {
        min-width: 42px;
        height: 42px;
        border-radius: 12px;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: #DBEAFE !important;
        color: #1D4ED8 !important;
        border: 1px solid #93C5FD;
        font-weight: 900 !important;
        font-size: 20px !important;
        box-shadow: 0 4px 12px rgba(37,99,235,.12);
    }

    .bio-arrow {
        height: 5px;
        border-radius: 999px;
        background: linear-gradient(90deg, #2563EB, #7C3AED);
        position: relative;
    }

    .bio-arrow::after {
        content: "";
        position: absolute;
        right: -1px;
        top: -7px;
        border-left: 14px solid #7C3AED;
        border-top: 9px solid transparent;
        border-bottom: 9px solid transparent;
    }

    .bio-process-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: .9rem;
        margin-top: 1rem;
    }

    .bio-step {
        display: flex;
        gap: .8rem;
        align-items: center;
        background: #F8FAFC;
        border: 1px solid #D8E2EF;
        border-radius: 16px;
        padding: 1rem;
        color: #334155 !important;
        font-size: 16px;
        line-height: 1.4;
        min-height: 78px;
    }

    .bio-step-index {
        width: 34px;
        height: 34px;
        border-radius: 10px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: #0B2454;
        color: #FFFFFF !important;
        font-size: 14px;
        font-weight: 900;
        flex: 0 0 auto;
    }

    .stop-grid {
        display: flex;
        gap: .75rem;
        overflow-x: auto;
        padding-bottom: .5rem;
    }

    .stop-card, .bio-empty-state {
        background: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 14px;
        padding: .95rem;
        color: #334155;
        font-weight: 700;
    }

    .stop-codon {
        color: #7C3AED;
        font-size: 24px;
        font-weight: 900;
        letter-spacing: .08em;
    }

    .stop-card small {
        color: #64748B;
        display: block;
        margin-top: .25rem;
    }

    @media (max-width: 900px) {
        .bio-flow {
            grid-template-columns: 1fr;
        }

        .bio-arrow {
            transform: rotate(90deg);
            width: 56px;
            justify-self: center;
        }

        .bio-token {
            min-width: 36px;
            height: 36px;
            font-size: 17px !important;
        }
    }
    </style>
    """)


def render_transcription_result(result, stop_codons):
    render_transcription_styles()

    st.html(f"""
    <div class="bio-flow-panel">
        <div class="bio-flow-title">Flujo de transcripción</div>
        <div class="bio-flow">
            <div class="bio-node">
                <div class="bio-node-label">ADN limpio</div>
                <div class="bio-token-wrap">{_sequence_tokens(result["dna"])}</div>
            </div>

            <div class="bio-arrow"></div>

            <div class="bio-node bio-node-rna">
                <div class="bio-node-label">ARN mensajero</div>
                <div class="bio-token-wrap">{_sequence_tokens(result["rna"])}</div>
            </div>
        </div>
    </div>
    """)

    st.html(f"""
    <div class="bio-flow-panel">
        <div class="bio-flow-title">Pasos del proceso</div>
        <div class="bio-process-grid">
            {_step_cards(result["steps"])}
        </div>
    </div>
    """)

    st.html(f"""
    <div class="bio-flow-panel">
        <div class="bio-flow-title">Codones de parada</div>
        <div class="stop-grid">
            {_stop_codon_cards(stop_codons)}
        </div>
    </div>
    """)


def transcription_page():
    load_styles()
    top_bar()

    disease_key = st.session_state.get("selected_disease", "huntington")
    disease = DISEASE_DATA[disease_key]

    st.title("Transcripción de ADN")
    st.subheader(disease["title"])

    st.markdown(
        "<p style='font-size: 14.5px; font-weight: 600; color: #475569; margin-bottom: 8px;'>Fuente de la secuencia</p>",
        unsafe_allow_html=True
    )

    if "transcription_source" not in st.session_state:
        st.session_state["transcription_source"] = "Secuencia del ejemplo"

    fuente_seq = st.radio(
        label="Fuente de la secuencia",
        options=["Secuencia del ejemplo", "Buscar en NCBI (Exploratorio)"],
        index=0 if st.session_state["transcription_source"] == "Secuencia del ejemplo" else 1,
        horizontal=True,
        label_visibility="collapsed"
    )

    if fuente_seq != st.session_state["transcription_source"]:
        st.session_state["transcription_source"] = fuente_seq

        if fuente_seq == "Secuencia del ejemplo":
            st.session_state.pop("transcription_ncbi", None)
            st.session_state["transcription_dna"] = disease.get(
                "mutated_sequence",
                disease["reference_sequence"]
            ).replace(" ", "")

        st.rerun()

    dna = disease.get("mutated_sequence", disease["reference_sequence"]).replace(" ", "")
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
                st.warning("Por favor, ingresa un Accession ID.")

    dna = st.text_area("Secuencia de ADN", value=dna, height=120)
    st.session_state["transcription_dna"] = dna

    if st.button("Transcribir ADN a ARN", type="primary"):
        is_valid, dna_clean = validate_dna_sequence(dna)

        if not is_valid:
            render_validation_error(dna_clean)
            st.stop()

        result = transcribe_dna_to_rna(dna_clean)
        stop_codons = find_stop_codons(result["rna"])

        render_transcription_result(result, stop_codons)

        if not st.session_state.get("completed_transcription", False):
            increment = 15
            st.session_state.progress = min(100, st.session_state.get("progress", 0) + increment)
            st.session_state.completed_transcription = True

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
            st.subheader("Información NCBI / FASTA")
            st.write(f"ID de acceso: {ncbi_data['id']}")
            st.write(f"Descripción: {ncbi_data['description']}")
            st.write(f"Fuente de datos: {ncbi_data['source']}")
            if "length" in ncbi_data:
                st.write(f"Longitud de la secuencia: {ncbi_data['length']} pb")

    if st.button("Volver", type="secondary", use_container_width=True):
        st.session_state.page = "disease_detail"
        st.rerun()