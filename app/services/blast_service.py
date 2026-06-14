def normalize_sequence(sequence: str) -> str:
    return (
        sequence.replace(" ", "")
        .replace("\n", "")
        .replace("\r", "")
        .upper()
    )


def global_alignment(reference: str, query: str) -> dict:
    ref = normalize_sequence(reference)
    qry = normalize_sequence(query)

    match_score = 2
    mismatch_score = -1
    gap_score = -2

    rows = len(ref) + 1
    cols = len(qry) + 1

    score = [[0 for _ in range(cols)] for _ in range(rows)]
    trace = [[None for _ in range(cols)] for _ in range(rows)]

    for i in range(1, rows):
        score[i][0] = i * gap_score
        trace[i][0] = "up"

    for j in range(1, cols):
        score[0][j] = j * gap_score
        trace[0][j] = "left"

    for i in range(1, rows):
        for j in range(1, cols):
            diagonal = score[i - 1][j - 1] + (
                match_score if ref[i - 1] == qry[j - 1] else mismatch_score
            )
            up = score[i - 1][j] + gap_score
            left = score[i][j - 1] + gap_score

            best = max(diagonal, up, left)
            score[i][j] = best

            if best == diagonal:
                trace[i][j] = "diag"
            elif best == up:
                trace[i][j] = "up"
            else:
                trace[i][j] = "left"

    aligned_ref = []
    aligned_qry = []
    match_line = []

    i = len(ref)
    j = len(qry)

    while i > 0 or j > 0:
        direction = trace[i][j]

        if direction == "diag":
            base_ref = ref[i - 1]
            base_qry = qry[j - 1]

            aligned_ref.append(base_ref)
            aligned_qry.append(base_qry)
            match_line.append("|" if base_ref == base_qry else "*")

            i -= 1
            j -= 1

        elif direction == "up":
            aligned_ref.append(ref[i - 1])
            aligned_qry.append("-")
            match_line.append(" ")
            i -= 1

        else:
            aligned_ref.append("-")
            aligned_qry.append(qry[j - 1])
            match_line.append(" ")
            j -= 1

    aligned_ref = "".join(reversed(aligned_ref))
    aligned_qry = "".join(reversed(aligned_qry))
    match_line = "".join(reversed(match_line))

    matches = match_line.count("|")
    mismatches = match_line.count("*")
    gaps = aligned_ref.count("-") + aligned_qry.count("-")

    identity = round((matches / len(match_line)) * 100, 2) if match_line else 0

    return {
        "reference": ref,
        "query": qry,
        "aligned_reference": aligned_ref,
        "aligned_query": aligned_qry,
        "match_line": match_line,
        "score": score[-1][-1],
        "matches": matches,
        "mismatches": mismatches,
        "gaps": gaps,
        "identity_percent": identity
    }


def count_repeated_pattern(sequence: str, pattern: str) -> int:
    sequence = normalize_sequence(sequence)
    pattern = pattern.upper()
    return sequence.count(pattern)


def analyze_disease_pattern(reference: str, query: str, disease_key: str) -> dict:
    ref = normalize_sequence(reference)
    qry = normalize_sequence(query)

    if disease_key == "huntington":
        cag_reference = count_repeated_pattern(ref, "CAG")
        cag_query = count_repeated_pattern(qry, "CAG")

        if cag_query > cag_reference:
            interpretation = "Expansión de repeticiones CAG detectada."
        elif cag_query < cag_reference:
            interpretation = "Reducción de repeticiones CAG detectada."
        else:
            interpretation = "No hubo cambio en el número de repeticiones CAG."

        return {
            "disease": "Huntington",
            "pattern": "Repeticiones CAG",
            "reference_value": cag_reference,
            "query_value": cag_query,
            "interpretation": interpretation
        }

    if disease_key == "anemia_falciforme":
        has_reference_pattern = "GAG" in ref
        has_mutated_pattern = "GTG" in qry

        if has_reference_pattern and has_mutated_pattern:
            interpretation = (
                "Se detectó un cambio compatible con GAG → GTG, "
                "patrón asociado a anemia falciforme."
            )
        else:
            interpretation = (
                "No se detectó claramente el patrón GAG → GTG "
                "en el fragmento analizado."
            )

        return {
            "disease": "Anemia falciforme",
            "pattern": "Sustitución GAG → GTG",
            "reference_value": "GAG presente" if has_reference_pattern else "GAG no detectado",
            "query_value": "GTG presente" if has_mutated_pattern else "GTG no detectado",
            "interpretation": interpretation
        }

    if disease_key == "fibrosis_quistica":
        deletion_detected = len(qry) < len(ref)

        if deletion_detected:
            interpretation = "Se detectó una deleción compatible con pérdida de bases en el gen CFTR."
        else:
            interpretation = "No se detectó una deleción evidente en el fragmento analizado."

        return {
            "disease": "Fibrosis quística",
            "pattern": "Deleción en CFTR",
            "reference_value": len(ref),
            "query_value": len(qry),
            "interpretation": interpretation
        }

    return {
        "disease": "No especificada",
        "pattern": "General",
        "reference_value": "-",
        "query_value": "-",
        "interpretation": "No se aplicó análisis específico por enfermedad."
    }


def detect_mutations(reference: str, query: str, disease_key: str = "huntington") -> dict:
    alignment = global_alignment(reference, query)

    aligned_ref = alignment["aligned_reference"]
    aligned_qry = alignment["aligned_query"]

    mutations = []
    ref_position = 0
    query_position = 0

    for index in range(len(aligned_ref)):
        base_ref = aligned_ref[index]
        base_qry = aligned_qry[index]

        if base_ref != "-":
            ref_position += 1

        if base_qry != "-":
            query_position += 1

        if base_ref == base_qry:
            continue

        if base_ref == "-":
            mutations.append({
                "type": "Inserción",
                "position": query_position,
                "reference_base": "-",
                "mutated_base": base_qry
            })

        elif base_qry == "-":
            mutations.append({
                "type": "Deleción",
                "position": ref_position,
                "reference_base": base_ref,
                "mutated_base": "-"
            })

        else:
            mutations.append({
                "type": "Sustitución",
                "position": ref_position,
                "reference_base": base_ref,
                "mutated_base": base_qry
            })

    special_finding = analyze_disease_pattern(reference, query, disease_key)

    steps = [
        "1. Se recibió una secuencia referencial y una secuencia mutada.",
        "2. Se limpiaron ambas secuencias eliminando espacios y saltos de línea.",
        "3. Se aplicó un alineamiento global tipo BLAST educativo.",
        "4. Se compararon las bases alineadas una por una.",
        "5. Se clasificaron las diferencias como sustitución, inserción o deleción.",
        "6. Se evaluó el patrón genético principal de la enfermedad seleccionada.",
        "7. Se generó una interpretación educativa del resultado."
    ]

    return {
        "alignment": alignment,
        "mutations": mutations,
        "mutation_count": len(mutations),
        "special_finding": special_finding,
        "steps": steps
    }