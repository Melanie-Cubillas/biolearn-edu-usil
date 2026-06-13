import streamlit as st
import pandas as pd
from Bio.Seq import Seq

from components.layout import load_styles, top_bar
from pages.disease_detail import DISEASE_DATA


def split_codons(rna: str) -> list:
    return [
        rna[i:i + 3]
        for i in range(0, len(rna), 3)
        if len(rna[i:i + 3]) == 3
    ]


def translation_page():
    load_styles()
    top_bar()

    disease_key = st.session_state.get("selected_disease", "huntington")
    disease = DISEASE_DATA[disease_key]

    st.title("Traducción")
    st.subheader(disease["title"])

    dna = st.text_input(
        "Secuencia de ADN",
        value=disease["mutated_sequence"].replace(" ", "")
    )

    clean_dna = dna.replace(" ", "").upper()
    rna = clean_dna.replace("T", "U")
    codons = split_codons(rna)

    try:
        protein = str(Seq(clean_dna).translate(to_stop=True))
    except Exception:
        protein = "No se pudo traducir la secuencia."

    st.write("**Codones del ARN:**")
    st.code(" | ".join(codons))

    st.write("**Proteína resultante:**")
    st.code(protein)

    df = pd.DataFrame({
        "Codón": codons,
        "Aminoácido": [str(Seq(c.replace("U", "T")).translate()) for c in codons]
    })

    st.subheader("Conversión a aminoácidos")
    st.dataframe(df, use_container_width=True)

    st.info(
        "La traducción es el proceso mediante el cual los codones del ARN "
        "se convierten en aminoácidos para formar proteínas."
    )

    if st.button("Volver"):
        st.session_state.page = "disease_detail"
        st.rerun()
