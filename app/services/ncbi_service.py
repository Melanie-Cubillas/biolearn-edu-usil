from pathlib import Path
from io import StringIO
import os
import re

from Bio import Entrez, SeqIO


Entrez.email = os.getenv("NCBI_EMAIL", "illaricubillas146@gmail.com")

APP_DIR = Path(__file__).resolve().parents[1]
FASTA_DIR = APP_DIR / "data" / "fasta"
FASTA_DIR.mkdir(parents=True, exist_ok=True)


def clean_accession_id(accession_id: str) -> str:
    return accession_id.strip().replace(" ", "")


def safe_filename(accession_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", accession_id)


def get_fasta_path(accession_id: str) -> Path:
    accession_id = safe_filename(clean_accession_id(accession_id))
    return FASTA_DIR / f"{accession_id}.fasta"


def parse_fasta_text(fasta_text: str, source: str, file_path: str = "") -> dict:
    record = SeqIO.read(StringIO(fasta_text), "fasta")

    return {
        "id": record.id,
        "description": record.description,
        "sequence": str(record.seq).upper(),
        "length": len(record.seq),
        "source": source,
        "file_path": file_path,
        "raw_fasta": fasta_text
    }


def read_local_fasta(accession_id: str) -> dict:
    fasta_path = get_fasta_path(accession_id)

    with open(fasta_path, "r", encoding="utf-8") as file:
        fasta_text = file.read()

    return parse_fasta_text(
        fasta_text=fasta_text,
        source="LOCAL_FASTA",
        file_path=str(fasta_path)
    )


def download_fasta_from_ncbi(accession_id: str, db: str = "nucleotide") -> str:
    accession_id = clean_accession_id(accession_id)

    handle = Entrez.efetch(
        db=db,
        id=accession_id,
        rettype="fasta",
        retmode="text"
    )

    fasta_text = handle.read()
    handle.close()

    if not fasta_text.strip().startswith(">"):
        raise ValueError("NCBI no devolvió un archivo FASTA válido.")

    return fasta_text


def save_fasta(accession_id: str, fasta_text: str) -> Path:
    fasta_path = get_fasta_path(accession_id)

    with open(fasta_path, "w", encoding="utf-8") as file:
        file.write(fasta_text)

    return fasta_path


def get_sequence(accession_id: str, db: str = "nucleotide") -> dict:
    accession_id = clean_accession_id(accession_id)
    fasta_path = get_fasta_path(accession_id)

    steps = []

    steps.append(f"1. Se recibió el Accession ID: {accession_id}")
    steps.append("2. Se verificó si la secuencia ya existe en FASTA local.")

    if fasta_path.exists():
        data = read_local_fasta(accession_id)
        steps.append("3. La secuencia ya existía localmente, no se llamó a NCBI.")
        steps.append("4. Se leyó el archivo FASTA guardado.")
        data["steps"] = steps
        return data

    steps.append("3. No se encontró FASTA local, se consultó NCBI.")
    fasta_text = download_fasta_from_ncbi(accession_id, db=db)

    steps.append("4. NCBI devolvió la secuencia en formato FASTA.")
    save_path = save_fasta(accession_id, fasta_text)

    steps.append("5. La secuencia se guardó localmente para futuras consultas.")

    data = parse_fasta_text(
        fasta_text=fasta_text,
        source="NCBI",
        file_path=str(save_path)
    )

    data["steps"] = steps
    return data
