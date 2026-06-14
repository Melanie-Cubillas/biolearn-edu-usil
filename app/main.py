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
    layout="wide"
)

if "page" not in st.session_state:
    st.session_state.page = "login"

if "user" not in st.session_state:
    st.session_state.user = None

if "selected_disease" not in st.session_state:
    st.session_state.selected_disease = "huntington"


if st.session_state.page == "login":
    login_page()

elif st.session_state.page == "register":
    register_page()

elif st.session_state.page == "dashboard":
    dashboard_page()

elif st.session_state.page == "diseases":
    diseases_page()

elif st.session_state.page == "disease_detail":
    disease_detail_page()

elif st.session_state.page == "quiz":
    quiz_page()

elif st.session_state.page == "tutorials":
    tutorials_page()

elif st.session_state.page == "translation":
    translation_page()

elif st.session_state.page == "transcription":
    transcription_page()

elif st.session_state.page == "mutation_recognition":
    mutation_recognition_page()

else:
    st.session_state.page = "login"
    st.rerun()