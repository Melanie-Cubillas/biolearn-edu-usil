import streamlit as st

from components.layout import load_styles, top_bar


DISEASE_DATA = {
    "huntington": {
        "title": "Enfermedad de Huntington",
        "category": "Neurodegenerativa",
        "gene": "HTT",
        "accession_id": "NM_002111",
        "mutation_pattern": "Repetición CAG",
        "concept": "Trastorno neurodegenerativo hereditario causado por la expansión anormal de tripletes CAG en el gen HTT. Esta mutación genera una proteína huntingtina alterada que afecta principalmente neuronas del cuerpo estriado.",
        "symptoms": [
            "Movimientos involuntarios (corea)",
            "Dificultad para coordinar movimientos",
            "Problemas de equilibrio y marcha",
            "Deterioro cognitivo progresivo",
            "Pérdida de memoria y concentración",
            "Cambios de personalidad",
            "Ansiedad y depresión",
        ],
        "causes": [
            "Mutación genética en el gen HTT del cromosoma 4.",
            "Expansión patológica de 40 o más tripletes CAG.",
            "Acumulación tóxica de la proteína huntingtina mutada.",
            "Muerte progresiva de neuronas en regiones cerebrales específicas.",
        ],
        "reference_sequence": "ATGGCGACCCTGGAAAAGCTGATGAAGGCCTTCGAGTCCCTCAAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAAGTCCCTGGAGACTCCAGTGGAAGC",
        "mutated_sequence": "ATGGCGACCCTGGAAAAGCTGATGAAGGCCTTCGAGTCCCTCAAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAAGTCCCTGGAGACTCCAGTGGAAGC",
    },
    "anemia_falciforme": {
        "title": "Anemia falciforme",
        "category": "Hematológica",
        "gene": "HBB",
        "accession_id": "NM_000518",
        "mutation_pattern": "GAG → GTG",
        "concept": "Enfermedad hematológica hereditaria autosómica recesiva, causada por una mutación puntual en el gen HBB. Produce hemoglobina S, la cual puede deformar los eritrocitos bajo condiciones de baja oxigenación.",
        "symptoms": [
            "Fatiga",
            "Dolor recurrente",
            "Anemia",
            "Infecciones frecuentes",
            "Problemas circulatorios",
            "Dificultad respiratoria",
        ],
        "causes": [
            "Mutación puntual por cambio de adenina por timina en el gen HBB.",
            "Cambio del codón GAG por GTG.",
            "Sustitución del ácido glutámico por valina.",
            "Patrón de herencia autosómico recesivo.",
        ],
        "reference_sequence": "ATGGTGCACCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAG",
        "mutated_sequence": "ATGGTGCACCTGACTCCTGTGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAG",
    },
    "fibrosis_quistica": {
        "title": "Fibrosis quística",
        "category": "Respiratoria y digestiva",
        "gene": "CFTR",
        "accession_id": "NM_000492",
        "mutation_pattern": "ΔF508",
        "concept": "Enfermedad genética autosómica recesiva causada por mutaciones en el gen CFTR. Estas alteraciones afectan el transporte de cloro y agua, generando secreciones espesas en pulmones, páncreas y otros órganos.",
        "symptoms": [
            "Tos persistente",
            "Infecciones respiratorias recurrentes",
            "Mucosidad espesa",
            "Dificultad respiratoria",
            "Problemas digestivos",
            "Malabsorción de nutrientes",
            "Sudor con alta concentración de sal",
        ],
        "causes": [
            "Mutación en el gen CFTR localizado en el cromosoma 7.",
            "Deleción de tres nucleótidos asociada a ΔF508.",
            "Pérdida del aminoácido fenilalanina en la posición 508.",
            "Alteración del transporte de cloro y agua en células epiteliales.",
        ],
        "reference_sequence": "ATCATCTTTGGTGTTTCCTATGATGAATATAG",
        "mutated_sequence": "ATCATCGGTGTTTCCTATGATGAATATAG",
    },
}


def render_page_styles():
    st.markdown("""
    <style>
    .detail-hero {
        background: linear-gradient(135deg, #EDE9FE 0%, #F3E8FF 100%);
        border-radius: 34px;
        padding: 3rem;
        margin-bottom: 2.5rem;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(226,232,240,.7);
    }

    .hero-tags {
        display: flex;
        gap: .7rem;
        flex-wrap: wrap;
        margin-bottom: 1.2rem;
    }

    .hero-tag {
        background: white;
        color: #334155;
        padding: .45rem .8rem;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 900;
        letter-spacing: .05em;
        text-transform: uppercase;
    }

    .detail-title {
        font-size: 56px;
        line-height: 1.05;
        color: #0F172A;
        font-weight: 900;
        margin-bottom: 1rem;
    }

    .detail-subtitle {
        color: #64748B;
        font-size: 20px;
        line-height: 1.55;
        max-width: 850px;
    }

    .info-card {
        background: rgba(255,255,255,.94);
        border: 1px solid #E2E8F0;
        border-radius: 28px;
        padding: 2rem;
        min-height: 360px;
        box-shadow: 0 14px 32px rgba(15,23,42,.05);
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .info-icon {
        width: 58px;
        height: 58px;
        border-radius: 999px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 27px;
        margin-bottom: .5rem;
    }

    .icon-purple { background:#EDE9FE; }
    .icon-blue { background:#E0F2FE; }
    .icon-green { background:#DCFCE7; }

    .info-card-title {
        color: #0F172A;
        font-size: 22px;
        font-weight: 900;
        margin: 0;
    }

    .info-card-text,
    .info-card li {
        color: #475569;
        font-size: 16px;
        line-height: 1.55;
    }

    .info-card ul {
        padding-left: 1.2rem;
        margin: 0;
    }

    .info-card li {
        margin-bottom: .55rem;
    }

    .section-kicker {
        color:#2563EB;
        font-size:14px;
        font-weight:900;
        letter-spacing:.12em;
        text-transform:uppercase;
        margin-top:2.8rem;
    }

    .section-title {
        color:#0F172A;
        font-size:34px;
        font-weight:900;
        margin-bottom:1.5rem;
    }

    .sequence-card {
        background: rgba(255,255,255,.92);
        border: 1px solid #E2E8F0;
        border-radius: 28px;
        padding: 2rem;
        box-shadow: 0 14px 32px rgba(15,23,42,.05);
        margin-bottom: 1.4rem;
    }

    .sequence-label {
        color:#475569;
        font-weight:900;
        letter-spacing:.12em;
        font-size:14px;
        text-transform:uppercase;
        margin-bottom:1rem;
    }

    .dna-wrap {
        display:flex;
        flex-wrap:wrap;
        gap:6px;
    }

    .base {
        width:38px;
        height:44px;
        border-radius:8px;
        display:flex;
        align-items:center;
        justify-content:center;
        font-weight:900;
        font-size:16px;
    }

    .base-A { background:#DCFCE7; color:#16A34A; }
    .base-T { background:#FEE2E2; color:#DC2626; }
    .base-C { background:#DBEAFE; color:#2563EB; }
    .base-G { background:#FED7AA; color:#EA580C; }

    .base-mut {
        background: linear-gradient(135deg, #8B5CF6, #A78BFA) !important;
        color: white !important;
        border: 2px solid #7C3AED !important;
        box-shadow: 0 0 12px rgba(139,92,246,.45);
        transform: scale(1.08);
    }

    .legend {
        display:flex;
        gap:.8rem;
        flex-wrap:wrap;
        margin-top:1rem;
        color:#475569;
        font-size:14px;
    }

    .action-title {
        color:#0F172A;
        font-size:30px;
        font-weight:900;
        margin-top:2.5rem;
        margin-bottom:1rem;
    }

    @media (max-width: 900px) {
        .detail-title {
            font-size: 38px;
        }

        .detail-hero {
            padding: 2rem;
        }

        .base {
            width:30px;
            height:36px;
            font-size:13px;
        }

        .info-card {
            min-height: auto;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def to_li(items):
    if isinstance(items, list):
        return "".join(f"<li>{item.replace('- ', '')}</li>" for item in items)
    return f"<li>{items}</li>"


def render_info_card(icon, icon_class, title, content):
    if isinstance(content, list):
        body = f"<ul>{to_li(content)}</ul>"
    else:
        body = f'<div class="info-card-text">{content}</div>'

    st.markdown(f"""
    <div class="info-card">
        <div class="info-icon {icon_class}">{icon}</div>
        <div class="info-card-title">{title}</div>
        {body}
    </div>
    """, unsafe_allow_html=True)


def base_class(base, is_mutation=False):
    class_name = f"base base-{base}"
    if is_mutation:
        class_name += " base-mut"
    return class_name


def get_highlight_indices(sequence, mutation_pattern):
    sequence = sequence.upper().replace(" ", "")
    indices = set()

    if mutation_pattern in ["CAG", "Repetición CAG"]:
        for i in range(0, len(sequence) - 2):
            if sequence[i:i + 3] == "CAG":
                indices.update([i, i + 1, i + 2])

    elif mutation_pattern in ["GAG → GTG", "GAG>GTG"]:
        for pattern in ["GAG", "GTG"]:
            start = sequence.find(pattern)
            if start != -1:
                indices.update([start, start + 1, start + 2])

    elif mutation_pattern in ["ΔF508", "Deleción F508"]:
        for pattern in ["TTT", "CTT"]:
            start = sequence.find(pattern)
            if start != -1:
                indices.update([start, start + 1, start + 2])

    return indices


def render_sequence(sequence, label, mutation_pattern=None):
    sequence = sequence.upper().replace(" ", "")
    mutation_indices = get_highlight_indices(sequence, mutation_pattern)

    bases_html = ""

    for index, base in enumerate(sequence):
        is_mut = index in mutation_indices
        bases_html += f'<div class="{base_class(base, is_mut)}">{base}</div>'

    st.markdown(f"""
    <div class="sequence-card">
        <div class="sequence-label">{label}</div>
        <div class="dna-wrap">
            {bases_html}
        </div>
        <div class="legend">
            <span>🟩 A = Adenina</span>
            <span>🟥 T = Timina</span>
            <span>🟦 C = Citosina</span>
            <span>🟧 G = Guanina</span>
            <span>🟪 Región clave/mutación</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def disease_detail_page():
    load_styles()
    render_page_styles()
    top_bar()

    disease_key = st.session_state.get("selected_disease", "huntington")
    disease = DISEASE_DATA[disease_key]

    st.markdown(f"""
    <div class="detail-hero">
        <div class="hero-tags">
            <span class="hero-tag">{disease["category"]}</span>
            <span class="hero-tag">Gen · {disease["gene"]}</span>
            <span class="hero-tag">{disease["mutation_pattern"]}</span>
        </div>
        <div class="detail-title">{disease["title"]}</div>
        <div class="detail-subtitle">{disease["concept"]}</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        render_info_card("🧠", "icon-purple", "Concepto médico y genético", disease["concept"])

    with col2:
        render_info_card("🩺", "icon-blue", "Síntomas", disease["symptoms"])

    with col3:
        render_info_card("❕", "icon-green", "Causas", disease["causes"])

    st.markdown('<div class="section-kicker">Secuencias</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Comparación de ADN</div>', unsafe_allow_html=True)

    render_sequence(
        disease["reference_sequence"],
        "Secuencia de referencia",
        disease["mutation_pattern"],
    )

    if disease.get("mutated_sequence"):
        render_sequence(
            disease["mutated_sequence"],
            "Secuencia mutada",
            disease["mutation_pattern"],
        )

    st.markdown('<div class="action-title">¿Qué te gustaría realizar?</div>', unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3, gap="large")

    with col_a:
        if st.button("Traducción", use_container_width=True):
            st.session_state.page = "translation"
            st.rerun()

    with col_b:
        if st.button("Transcripción", use_container_width=True):
            st.session_state.page = "transcription"
            st.rerun()

    with col_c:
        if st.button("Reconocer mutaciones", use_container_width=True):
            st.session_state.page = "mutation_recognition"
            st.rerun()

    st.divider()

    if st.button("Volver a enfermedades"):
        st.session_state.page = "diseases"
        st.rerun()