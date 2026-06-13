import streamlit as st
from components.layout import load_styles, top_bar


DISEASES = [
    {
        "name": "Enfermedad de Huntington",
        "key": "huntington",
        "description": "Trastorno genético causado por repeticiones CAG en el gen HTT."
    },
    {
        "name": "Anemia falciforme",
        "key": "anemia_falciforme",
        "description": "Enfermedad hereditaria que afecta la hemoglobina y la forma de los glóbulos rojos."
    },
    {
        "name": "Fibrosis quística",
        "key": "fibrosis_quistica",
        "description": "Enfermedad genética relacionada con mutaciones en el gen CFTR."
    }
]


def diseases_page():
    load_styles()
    top_bar()

    st.title("Aprender sobre Bioinformática")
    st.subheader("¿Sobre qué enfermedad te gustaría aprender?")

    cols = st.columns(3)

    for index, disease in enumerate(DISEASES):
        with cols[index]:
            with st.container(border=True):
                st.markdown(f"### {disease['name']}")
                st.write(disease["description"])

                if st.button("Aprender", key=disease["key"], use_container_width=True):
                    st.session_state.selected_disease = disease["key"]
                    st.session_state.page = "disease_detail"
                    st.rerun()

    if st.button("Volver al inicio"):
        st.session_state.page = "dashboard"
        st.rerun()
