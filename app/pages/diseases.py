import streamlit as st
from components.layout import load_styles, top_bar


DISEASES = [
    {
        "name": "Enfermedad de Huntington",
        "key": "huntington",
        "icon": "🧬",
        "tag": "Gen HTT",
        "description": "Trastorno genético causado por repeticiones CAG en el gen HTT.",
        "color": "#E0F2FE",
        "border": "#BAE6FD"
    },
    {
        "name": "Anemia falciforme",
        "key": "anemia_falciforme",
        "icon": "🩸",
        "tag": "Gen HBB",
        "description": "Enfermedad hereditaria que afecta la hemoglobina y la forma de los glóbulos rojos.",
        "color": "#FCE7F3",
        "border": "#FBCFE8"
    },
    {
        "name": "Fibrosis quística",
        "key": "fibrosis_quistica",
        "icon": "🫁",
        "tag": "Gen CFTR",
        "description": "Enfermedad genética relacionada con mutaciones en el gen CFTR.",
        "color": "#DCFCE7",
        "border": "#BBF7D0"
    }
]


def disease_card(disease):
    st.markdown(f"""
    <div style="
        min-height:300px;
        background:{disease['color']};
        border:1px solid {disease['border']};
        border-radius:28px;
        padding:2rem;
        box-shadow:0 12px 28px rgba(15,23,42,.05);
        display:flex;
        flex-direction:column;
        justify-content:space-between;
    ">
        <div>
            <div style="
                width:58px;
                height:58px;
                border-radius:20px;
                background:white;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:30px;
                margin-bottom:1.2rem;
            ">
                {disease['icon']}
            </div>

            <h3 style="
                color:#0F172A;
                font-size:28px;
                margin:0 0 1rem 0;
                line-height:1.15;
            ">
                {disease['name']}
            </h3>

            <p style="
                color:#475569;
                font-size:17px;
                line-height:1.55;
                margin-bottom:1.2rem;
            ">
                {disease['description']}
            </p>

            <span style="
                background:white;
                color:#334155;
                border:1px solid #E2E8F0;
                padding:.45rem .9rem;
                border-radius:999px;
                font-weight:700;
                font-size:14px;
            ">
                {disease['tag']}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Aprender", key=disease["key"], use_container_width=True):
        st.session_state.selected_disease = disease["key"]
        st.session_state.progress = max(st.session_state.get("progress", 0), 20)
        st.session_state.page = "disease_detail"
        st.rerun()


def diseases_page():
    load_styles()
    top_bar()

    st.markdown("""
    <h1 style="
        font-size:46px;
        font-weight:900;
        color:#1F2937;
        margin-bottom:.5rem;
    ">
        Aprender sobre Bioinformática
    </h1>

    <p style="
        font-size:20px;
        color:#64748B;
        margin-bottom:2rem;
    ">
        Elige una enfermedad genética para explorar su base molecular, secuencias y mutaciones.
    </p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        disease_card(DISEASES[0])

    with col2:
        disease_card(DISEASES[1])

    with col3:
        disease_card(DISEASES[2])

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Volver al inicio", use_container_width=False):
        st.session_state.page = "dashboard"
        st.rerun()