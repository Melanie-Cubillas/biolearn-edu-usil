import streamlit as st

from components.layout import load_styles, top_bar
from pages.disease_detail import DISEASE_DATA


def count_pattern(sequence: str, pattern: str) -> int:
    sequence = sequence.replace(" ", "").upper()
    pattern = pattern.upper()
    return sequence.count(pattern)


def detect_mutation(reference: str, mutated: str) -> dict:
    ref = reference.replace(" ", "").upper()
    mut = mutated.replace(" ", "").upper()

    if len(mut) > len(ref):
        mutation_type = "Inserción o expansión"
    elif len(mut) < len(ref):
        mutation_type = "Deleción"
    elif ref != mut:
        mutation_type = "Sustitución"
    else:
        mutation_type = "Sin mutación detectada"

    return {
        "reference": ref,
        "mutated": mut,
        "mutation_type": mutation_type,
        "length_reference": len(ref),
        "length_mutated": len(mut),
        "cag_reference": count_pattern(ref, "CAG"),
        "cag_mutated": count_pattern(mut, "CAG")
    }


def mutation_recognition_page():
    load_styles()
    top_bar()

    disease_key = st.session_state.get("selected_disease", "huntington")
    disease = DISEASE_DATA[disease_key]

    st.title("Reconocimiento de mutaciones")
    st.subheader(disease["title"])

    reference = st.text_input(
        "Secuencia referencial",
        value=disease["reference_sequence"]
    )

    mutated = st.text_input(
        "Secuencia mutada",
        value=disease["mutated_sequence"]
    )

    mode = st.radio(
        "Selecciona el modo",
        ["Modo guiado", "Modo exploratorio"],
        horizontal=True
    )

    if mode == "Modo exploratorio":
        st.selectbox(
            "Selecciona una opción",
            ["Secuencia 1", "Secuencia 2", "Secuencia 3"]
        )

        if st.button("Buscar en NCBI"):
            st.info("Aquí conectaremos luego el servicio NCBI + FASTA local.")

    if st.button("Reconocer mutaciones"):
        result = detect_mutation(reference, mutated)

        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.subheader("Estadísticas del alineamiento")
                st.write(f"Longitud referencial: {result['length_reference']}")
                st.write(f"Longitud mutada: {result['length_mutated']}")
                st.write(f"Tipo de mutación: {result['mutation_type']}")
                st.write(f"Repeticiones CAG referencial: {result['cag_reference']}")
                st.write(f"Repeticiones CAG mutada: {result['cag_mutated']}")

        with col2:
            with st.container(border=True):
                st.subheader("Comparación visual")
                st.write("Referencia:")
                st.code(result["reference"])
                st.write("Mutada:")
                st.code(result["mutated"])

        st.subheader("Interpretación")

        if result["cag_mutated"] > result["cag_reference"]:
            st.warning(
                "Se detectó un aumento de repeticiones CAG. "
                "En Huntington, una expansión excesiva de CAG puede alterar la proteína huntingtina."
            )
        elif result["mutation_type"] == "Sustitución":
            st.info("Se detectó una sustitución de bases entre ambas secuencias.")
        elif result["mutation_type"] == "Deleción":
            st.info("Se detectó una pérdida de bases en la secuencia mutada.")
        elif result["mutation_type"] == "Inserción o expansión":
            st.info("Se detectó una inserción o expansión en la secuencia mutada.")
        else:
            st.success("No se detectaron diferencias entre ambas secuencias.")

    if st.button("Volver"):
        st.session_state.page = "disease_detail"
        st.rerun()
