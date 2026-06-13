import streamlit as st
from components.layout import load_styles, top_bar


def tutorials_page():
    load_styles()
    top_bar()

    st.title("Tutoriales")

    st.write("Aprende a usar BioLearn paso a paso.")

    with st.expander("1. ¿Cómo iniciar sesión?"):
        st.write("""
        Ingresa tu correo institucional y contraseña. 
        Si aún no tienes cuenta, selecciona la opción de registro.
        """)

    with st.expander("2. ¿Cómo elegir una enfermedad?"):
        st.write("""
        Desde el inicio, selecciona 'Aprende sobre Bioinformática'. 
        Luego elige una enfermedad genética como Huntington, anemia falciforme o fibrosis quística.
        """)

    with st.expander("3. ¿Cómo reconocer mutaciones?"):
        st.write("""
        Ingresa una secuencia referencial y una secuencia mutada. 
        La plataforma comparará ambas secuencias y mostrará el tipo de alteración encontrada.
        """)

    with st.expander("4. ¿Cómo usar NCBI?"):
        st.write("""
        En el modo exploratorio, puedes buscar secuencias reales mediante un Accession ID. 
        La plataforma guardará el archivo FASTA localmente para no consultar NCBI repetidamente.
        """)

    with st.expander("5. ¿Cómo resolver el quiz?"):
        st.write("""
        Selecciona una respuesta por pregunta y presiona 'Enviar respuestas'. 
        Al final verás tu puntaje.
        """)

    if st.button("Volver al inicio"):
        st.session_state.page = "dashboard"
        st.rerun()
