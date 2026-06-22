import html
import re

import streamlit as st
import pandas as pd

from components.layout import load_styles, top_bar
from pages.disease_detail import DISEASE_DATA
from services.ncbi_service import get_sequence
from services.bioinformatics_service import translate_dna_to_protein


def _sequence_tokens(sequence, token_size=1, limit=180):
    sequence = (sequence or "")[:limit]
    return "".join(
        f"<span class='bio-token'>{html.escape(sequence[index:index + token_size])}</span>"
        for index in range(0, len(sequence), token_size)
    )


def _protein_tokens(protein, limit=80):
    protein = (protein or "")[:limit]
    return "".join(
        f"<span class='protein-token'>{html.escape(aminoacid)}</span>"
        for aminoacid in protein
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


def _codon_cards(codon_table):
    return "".join(
        f"""
        <div class="codon-card">
            <div class="codon-rna">{html.escape(item["codon_rna"])}</div>
            <div class="codon-link"></div>
            <div class="aminoacid-chip">{html.escape(item["aminoacid"])}</div>
            <small>ADN: {html.escape(item["codon_dna"])}</small>
        </div>
        """
        for item in codon_table
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


def render_translation_result(result, df):
    st.markdown(
        f"""
        <style>
        .bio-flow-panel {{
            background: #FFFFFF;
            border: 1px solid #D8E2EF;
            border-radius: 16px;
            padding: 1.35rem;
            margin: 1.25rem 0;
            box-shadow: 0 14px 32px rgba(15, 23, 42, 0.07);
        }}

        .bio-flow-title {{
            color: #061A3A;
            font-size: 20px;
            font-weight: 900;
            margin-bottom: 1rem;
        }}

        .bio-flow {{
            display: grid;
            grid-template-columns: minmax(0, 1fr) 56px minmax(0, 1fr) 56px minmax(0, 1fr);
            gap: 1rem;
            align-items: center;
        }}

        .bio-node {{
            min-height: 180px;
            border-radius: 14px;
            border: 1px solid #BFDBFE;
            background: linear-gradient(180deg, #F8FAFC 0%, #EFF6FF 100%);
            padding: 1rem;
            overflow: hidden;
        }}

        .bio-node-rna {{
            border-color: #C4B5FD;
            background: linear-gradient(180deg, #F8FAFC 0%, #F5F3FF 100%);
        }}

        .bio-node-protein {{
            border-color: #93C5FD;
            background: linear-gradient(180deg, #F8FAFC 0%, #EEF2FF 100%);
        }}

        .bio-node-label {{
            color: #2563EB;
            font-size: 12px;
            font-weight: 900;
            letter-spacing: .1em;
            text-transform: uppercase;
            margin-bottom: .7rem;
        }}

        .bio-token-wrap, .protein-token-wrap {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.35rem;
            max-height: 118px;
            overflow: auto;
            padding-right: 0.2rem;
        }}

        .bio-token, .protein-token {{
            min-width: 28px;
            height: 28px;
            border-radius: 8px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: #0B2454;
            color: #FFFFFF !important;
            font-weight: 900;
            font-size: 12px;
            box-shadow: inset 0 -2px 0 rgba(255, 255, 255, .12);
        }}

        .protein-token {{
            background: linear-gradient(135deg, #2563EB, #7C3AED);
            min-width: 32px;
        }}

        .bio-arrow {{
            height: 4px;
            border-radius: 999px;
            background: linear-gradient(90deg, #2563EB, #7C3AED);
            position: relative;
            overflow: hidden;
        }}

        .bio-arrow::before {{
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,.85), transparent);
            animation: bioPulse 1.4s linear infinite;
        }}

        .bio-arrow::after {{
            content: "";
            position: absolute;
            right: -1px;
            top: -6px;
            border-left: 12px solid #7C3AED;
            border-top: 8px solid transparent;
            border-bottom: 8px solid transparent;
        }}

        .bio-process-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: .75rem;
            margin-top: 1rem;
        }}

        .bio-step {{
            display: flex;
            gap: .65rem;
            align-items: flex-start;
            color: #334155;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: .8rem;
            font-size: 13.5px;
            line-height: 1.35;
        }}

        .bio-step-index {{
            width: 24px;
            height: 24px;
            border-radius: 8px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: #0B2454;
            color: #FFFFFF !important;
            font-size: 12px;
            font-weight: 900;
            flex: 0 0 auto;
        }}

        .codon-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(118px, 1fr));
            gap: .75rem;
            max-height: 330px;
            overflow: auto;
            padding-right: .25rem;
        }}

        .codon-card {{
            background: #F8FAFC;
            border: 1px solid #CBD5E1;
            border-radius: 12px;
            padding: .85rem;
            color: #334155;
        }}

        .codon-rna {{
            color: #0B2454;
            font-size: 18px;
            font-weight: 900;
            letter-spacing: .08em;
        }}

        .codon-link {{
            height: 3px;
            width: 44px;
            border-radius: 999px;
            background: linear-gradient(90deg, #2563EB, #7C3AED);
            margin: .5rem 0;
        }}

        .aminoacid-chip {{
            width: 32px;
            height: 32px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #312E81;
            color: #FFFFFF !important;
            font-weight: 900;
        }}

        .codon-card small {{
            display: block;
            color: #64748B;
            font-weight: 700;
            margin-top: .45rem;
        }}

        .stop-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: .75rem;
            margin-top: 1rem;
        }}

        .stop-card, .bio-empty-state {{
            background: #F8FAFC;
            border: 1px solid #CBD5E1;
            border-radius: 12px;
            padding: .9rem;
            color: #334155;
            font-weight: 700;
        }}

        .stop-codon {{
            color: #7C3AED;
            font-size: 24px;
            font-weight: 900;
            letter-spacing: .08em;
        }}

        .stop-card small {{
            color: #64748B;
            display: block;
            margin-top: .25rem;
        }}

        @keyframes bioPulse {{
            from {{ transform: translateX(-100%); }}
            to {{ transform: translateX(100%); }}
        }}

        @media (max-width: 900px) {{
            .bio-flow {{
                grid-template-columns: 1fr;
            }}
            .bio-arrow {{
                transform: rotate(90deg);
                width: 56px;
                justify-self: center;
            }}
        }}
        </style>

        <div class="bio-flow-panel">
            <div class="bio-flow-title">Flujo de traducción</div>
            <div class="bio-flow">
                <div class="bio-node">
                    <div class="bio-node-label">ADN</div>
                    <div class="bio-token-wrap">{_sequence_tokens(result["dna"])}</div>
                </div>
                <div class="bio-arrow"></div>
                <div class="bio-node bio-node-rna">
                    <div class="bio-node-label">ARNm generado</div>
                    <div class="bio-token-wrap">{_sequence_tokens(result["rna"])}</div>
                </div>
                <div class="bio-arrow"></div>
                <div class="bio-node bio-node-protein">
                    <div class="bio-node-label">Proteína</div>
                    <div class="protein-token-wrap">{_protein_tokens(result["protein"])}</div>
                </div>
            </div>

            <div class="bio-process-grid">
                {_step_cards(result["steps"])}
            </div>

            <div class="bio-flow-title" style="margin-top:1.2rem;">Conversión codón a aminoácido</div>
            <div class="codon-grid">
                {_codon_cards(df.to_dict("records"))}
            </div>

            <div class="bio-flow-title" style="margin-top:1.2rem;">Codones de parada</div>
            <div class="stop-grid">
                {_stop_codon_cards(result["stop_codons"])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
        if not re.fullmatch(r"[ACTG]+", dna or "", flags=re.IGNORECASE):
            st.toast("Secuencia inválida: usa únicamente A, C, T o G.", icon=":material/warning:")
            st.markdown(
                """
                <div style="
                    margin: 1rem 0;
                    padding: 1rem 1.1rem;
                    border-radius: 12px;
                    background: linear-gradient(135deg, #EFF6FF 0%, #EEF2FF 100%);
                    border: 1px solid #60A5FA;
                    color: #0B2454;
                    font-weight: 700;
                    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
                ">
                    Validación USIL: la secuencia de ADN solo puede contener los nucleótidos A, C, T y G.
                </div>
                """,
                unsafe_allow_html=True,
            )
            return

        result = translate_dna_to_protein(dna)
        df = pd.DataFrame(result["codon_table"])
        render_translation_result(result, df)

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
