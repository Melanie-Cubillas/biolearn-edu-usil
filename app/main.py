import streamlit as st

from pages.login import login_page
from pages.register import register_page
from pages.dashboard import dashboard_page
from pages.diseases import diseases_page
from pages.disease_detail import disease_detail_page
from pages.quiz import quiz_page
from pages.tutorials import tutorials_page
from pages.translation import translation_page
from pages.transcription import transcription_page
from pages.mutation_recognition import mutation_recognition_page

st.set_page_config(
    page_title="BioLearn Edu",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ocultar menú lateral automático de Streamlit
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
[data-testid="collapsedControl"] {
    display: none;
}
#MainMenu {
    visibility: hidden;
}
footer {
    visibility: hidden;
}
header {
    visibility: hidden;
}
.block-container {
    padding-top: 0rem;
}
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "login"

if "user" not in st.session_state:
    st.session_state.user = None

if "selected_disease" not in st.session_state:
    st.session_state.selected_disease = "huntington"

pages = {
    "login": login_page,
    "register": register_page,
    "dashboard": dashboard_page,
    "diseases": diseases_page,
    "disease_detail": disease_detail_page,
    "quiz": quiz_page,
    "tutorials": tutorials_page,
    "translation": translation_page,
    "transcription": transcription_page,
    "mutation_recognition": mutation_recognition_page,
}

pages.get(st.session_state.page, login_page)()