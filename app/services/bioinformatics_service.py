from Bio.Seq import Seq


STOP_CODONS = {"UAA", "UAG", "UGA"}


def clean_sequence(sequence: str) -> str:
    return (
        sequence.replace(" ", "")
        .replace("\n", "")
        .replace("\r", "")
        .upper()
    )


def keep_valid_dna(sequence: str) -> str:
    sequence = clean_sequence(sequence)
    valid = {"A", "T", "C", "G", "N"}
    return "".join(base for base in sequence if base in valid)


def transcribe_dna_to_rna(dna_sequence: str) -> dict:
    dna = keep_valid_dna(dna_sequence)
    rna = dna.replace("T", "U")

    steps = [
        "1. Se recibió una cadena de ADN.",
        "2. Se limpió la secuencia eliminando espacios y saltos de línea.",
        "3. Se convirtió la secuencia a mayúsculas.",
        "4. Se reemplazó cada Timina (T) por Uracilo (U).",
        "5. El resultado obtenido corresponde al ARN mensajero."
    ]

    return {
        "dna": dna,
        "rna": rna,
        "steps": steps
    }


def split_codons(rna_sequence: str) -> list:
    rna = clean_sequence(rna_sequence)

    return [
        rna[i:i + 3]
        for i in range(0, len(rna), 3)
        if len(rna[i:i + 3]) == 3
    ]


def find_stop_codons(rna_sequence: str) -> list:
    codons = split_codons(rna_sequence)
    found = []

    for index, codon in enumerate(codons):
        if codon in STOP_CODONS:
            found.append({
                "codon": codon,
                "codon_position": index + 1,
                "base_position": index * 3 + 1
            })

    return found


def translate_dna_to_protein(dna_sequence: str) -> dict:
    dna = keep_valid_dna(dna_sequence)
    rna = dna.replace("T", "U")
    codons = split_codons(rna)

    protein = str(Seq(dna).translate(to_stop=True))
    stop_codons = find_stop_codons(rna)

    codon_table = []

    for codon in codons:
        dna_codon = codon.replace("U", "T")
        aminoacid = str(Seq(dna_codon).translate())
        codon_table.append({
            "codon_rna": codon,
            "codon_dna": dna_codon,
            "aminoacid": aminoacid
        })

    steps = [
        "1. Se recibió una secuencia de ADN.",
        "2. Se limpió la secuencia y se conservaron bases válidas.",
        "3. Se transcribió ADN a ARN reemplazando T por U.",
        "4. Se dividió el ARN en grupos de tres bases llamados codones.",
        "5. Cada codón fue traducido a su aminoácido correspondiente.",
        "6. La traducción se detuvo si apareció un codón de parada."
    ]

    return {
        "dna": dna,
        "rna": rna,
        "codons": codons,
        "codon_table": codon_table,
        "protein": protein,
        "stop_codons": stop_codons,
        "steps": steps
    }


def get_dna_complement(dna_sequence: str) -> str:
    dna = keep_valid_dna(dna_sequence)
    table = str.maketrans("ATCGN", "TAGCN")
    return dna.translate(table)


def analyze_sequence(dna_sequence: str) -> dict:
    transcription = transcribe_dna_to_rna(dna_sequence)
    translation = translate_dna_to_protein(dna_sequence)
    complement = get_dna_complement(dna_sequence)

    return {
        "dna": transcription["dna"],
        "complement": complement,
        "rna": transcription["rna"],
        "codons": translation["codons"],
        "protein": translation["protein"],
        "codon_table": translation["codon_table"],
        "stop_codons": translation["stop_codons"],
        "length": len(transcription["dna"]),
        "steps": transcription["steps"] + translation["steps"]
    }