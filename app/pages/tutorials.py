import streamlit as st
from components.layout import load_styles, top_bar

TUTORIALS_DATA = {
    "bioinformatics_intro": {
        "title": "Introducción a la Bioinformática",
        "desc": "Conoce los fundamentos de la bioinformática y cómo une las ciencias biológicas con la computación.",
        "objective": "Comprender el rol del análisis computacional en la biología moderna.",
        "level": "Básico",
        "content": """
### 1. ¿Qué es la Bioinformática?

La **bioinformática** es una disciplina científica interdisciplinaria que utiliza la computación, la matemática aplicada y la estadística para gestionar, analizar y modelar datos biológicos.

#### Importancia
El desarrollo de la secuenciación de ADN de nueva generación (NGS) genera diariamente millones de secuencias. La bioinformática es indispensable para:
- Organizar grandes volúmenes de datos genómicos en bases de datos accesibles.
- Comparar secuencias para encontrar homologías evolutivas o mutaciones clínicas.
- Predecir la estructura y función tridimensional de macromoléculas (como proteínas).

#### Principales aplicaciones
- **Alineamiento de secuencias:** Comparar secuencias biológicas (ADN/ARN/Proteínas) para hallar similitudes.
- **Ensamblaje genómico:** Reconstruir genomas completos a partir de millones de lecturas cortas.
- **Anotación de genes:** Identificar regiones codificantes y funciones dentro de un genoma.
"""
    },
    "dna_arn_proteins": {
        "title": "Conceptos Básicos: ADN, ARN y Proteínas",
        "desc": "Estudia el flujo de información genética en la célula (el Dogma Central de la Biología Molecular).",
        "objective": "Identificar las diferencias estructurales y funcionales del ADN, ARN y proteínas.",
        "level": "Básico",
        "content": """
### 2. Conceptos Básicos: ADN, ARN y Proteínas

La vida se codifica en moléculas biológicas interconectadas mediante el flujo clásico de información genética.

#### ADN (Ácido Desoxirribonucleico)
- **Estructura:** Doble hélice formada por nucleótidos que contienen desoxirribosa, un grupo fosfato y una base nitrogenada.
- **Bases:** Adenina (A), Timina (T), Citosina (C) y Guanina (G).
- **Función:** Almacenar la información genética a largo plazo de forma estable.

#### ARN (Ácido Ribonucleico)
- **Estructura:** Hebra sencilla que contiene ribosa y un grupo fosfato.
- **Bases:** Reemplaza la Timina por el Uracilo (U). Las bases son A, U, C y G.
- **Función:** Actuar como mensajero y participante activo en la síntesis de proteínas.

#### Proteínas
- **Estructura:** Cadenas lineales de aminoácidos plegadas en estructuras específicas tridimensionales.
- **Función:** Realizar la mayor parte de las funciones estructurales, metabólicas y catalíticas en los seres vivos.
"""
    },
    "transcription_guide": {
        "title": "Transcripción: Del ADN al ARN",
        "desc": "Analiza cómo la célula copia la información del ADN en una cadena de ARN mensajero.",
        "objective": "Aprender las reglas de complementariedad y el proceso de transcripción.",
        "level": "Básico",
        "content": """
### 3. Transcripción: Del ADN al ARN

La **transcripción** es el primer paso de la expresión génica. En este proceso, una enzima llamada ARN polimerasa lee una hebra de ADN (plantilla) para sintetizar una molécula complementaria de ARN mensajero (ARNm).

#### Reglas de emparejamiento de bases
Durante la transcripción, las bases del ADN se emparejan con nucleótidos complementarios de ARN de la siguiente forma:
- La Adenina (**A**) en el ADN se aparea con el Uracilo (**U**) en el ARN.
- La Timina (**T**) en el ADN se aparea con la Adenina (**A**) en el ARN.
- La Citosina (**C**) en el ADN se aparea con la Guanina (**G**) en el ARN.
- La Guanina (**G**) en el ADN se aparea con la Citosina (**C**) en el ARN.

*Ejemplo:*
- ADN de molde: `5'- TAC GCG TTA -3'`
- ARN transcrito: `3'- AUG CGC AAU -5'` (invertido para mantener la dirección 5' a 3': `5'- UAA GCG CAU -3'` según la polaridad de lectura).
"""
    },
    "translation_guide": {
        "title": "Traducción: Síntesis de Proteínas",
        "desc": "Aprende cómo el código del ARN mensajero se traduce en una secuencia funcional de aminoácidos.",
        "objective": "Comprender el código genético, codones y el uso de la tabla de traducción.",
        "level": "Intermedio",
        "content": """
### 4. Traducción: Síntesis de Proteínas

La **traducción** es el proceso por el cual la secuencia de nucleótidos del ARNm se convierte en una cadena de aminoácidos (proteína). Ocurre en los ribosomas.

#### El Código Genético
- El código genético se lee en grupos de tres nucleótidos llamados **codones**.
- Cada codón codifica para un aminoácido específico o para una señal de parada.
- Existen $64$ codones posibles y solo $20$ aminoácidos estándar, por lo que el código genético es **degenerado** (múltiples codones pueden codificar para el mismo aminoácido).

#### Pasos Clave
1. **Inicio:** El ribosoma reconoce el codón de inicio (generalmente `AUG`, que codifica para Metionina).
2. **Elongación:** Los ARNt traen los aminoácidos correspondientes a cada codón subsiguiente.
3. **Parada:** La traducción finaliza al encontrarse un codón de parada (`UAA`, `UAG` o `UGA`), liberando la proteína sintetizada.
"""
    },
    "mutations_intro": {
        "title": "Mutaciones Genéticas y sus Tipos",
        "desc": "Estudia las variaciones en el ADN y cómo afectan la secuencia y estructura final de las proteínas.",
        "objective": "Clasificar las mutaciones puntuales: sustituciones, inserciones y deleciones.",
        "level": "Intermedio",
        "content": """
### 5. Mutaciones Genéticas y sus Tipos

Una **mutación** es cualquier cambio heredable en la secuencia de nucleótidos del ADN de un organismo. Las mutaciones son la fuente primaria de variabilidad genética, pero también pueden causar enfermedades.

#### Tipos de mutaciones puntuales
1. **Sustitución:** Cambio de un nucleótido por otro.
   - **Silenciosa:** No altera el aminoácido codificado.
   - **De sentido erróneo (missense):** Cambia un aminoácido por otro (ej. anemia falciforme: GAG a GTG).
   - **Sin sentido (nonsense):** Introduce un codón de parada prematuro, truncando la proteína.
2. **Inserción:** Adición de uno o más nucleótidos en la secuencia. Puede provocar un cambio en la pauta de lectura (frameshift).
3. **Deleción:** Pérdida de uno o más nucleótidos de la secuencia (ej. fibrosis quística: deleción delta F508).
"""
    },
    "fasta_format": {
        "title": "Secuencias y Formato FASTA",
        "desc": "Aprende el estándar computacional para almacenar y compartir secuencias biológicas en archivos de texto plano.",
        "objective": "Leer, estructurar e interpretar correctamente archivos en formato FASTA.",
        "level": "Básico",
        "content": """
### 6. Secuencias y Formato FASTA

El **formato FASTA** es un formato de archivo de texto plano utilizado para representar secuencias de nucleótidos o péptidos de forma compacta y estandarizada.

#### Estructura de un archivo FASTA
Consta de dos partes esenciales:
1. **Línea de encabezado:** Comienza siempre con el símbolo mayor que (`>`). Contiene el identificador de la secuencia y detalles opcionales (nombre, especie, gen, etc.).
2. **Línea de secuencia:** Una o más líneas de texto con las bases nitrogenadas (A, T, C, G, U) o los aminoácidos de la proteína (A, C, D, E, F...).

*Ejemplo:*
```text
>NM_000518.5 Homo sapiens hemoglobin subunit beta (HBB), mRNA
ATGGTGCACCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAAC
GTGGATGAAGTTGGTGGTGAGGCCCTGGGCAGGCTGCTGGTGGTCTACCCTTGGACCCAG
```
"""
    },
    "ncbi_databases": {
        "title": "Uso de Bases de Datos NCBI",
        "desc": "Conoce el Centro Nacional de Información Biotecnológica y cómo buscar secuencias genéticas con Accession IDs.",
        "objective": "Aprender a consultar genes e interpretar identificadores en GenBank.",
        "level": "Intermedio",
        "content": """
### 7. Uso de Bases de Datos NCBI y GenBank

El **NCBI** (National Center for Biotechnology Information) es la institución pública estadounidense que alberga las bases de datos de información biológica y genética más importantes a nivel global.

#### GenBank y los Accession IDs
Cada secuencia depositada en el NCBI recibe un identificador único global llamado **Accession ID** (ID de acceso). Este código no cambia con el tiempo y permite la reproducibilidad en la investigación científica.
- *Ejemplo de nucleótidos:* `NM_002111` (ARNm de la huntingtina en humanos).
- *Ejemplo de proteína:* `NP_002102`.

#### Búsqueda Efectiva
Al buscar en bases de datos como GenBank, los bioinformáticos descargan los archivos en formato FASTA o GenBank completo para extraer información clínica, referencias de publicaciones, secuencias codificantes (CDS) y variantes asociadas.
"""
    },
    "seq_interpretation": {
        "title": "Interpretación Biológica de Secuencias",
        "desc": "Integra los conceptos para analizar casos reales, identificando marcos de lectura y variantes mutacionales.",
        "objective": "Interpretar alineamientos locales y deducir implicancias patológicas.",
        "level": "Avanzado",
        "content": """
### 8. Interpretación Biológica de Secuencias

La interpretación biológica consiste en analizar una secuencia de nucleótidos para deducir su impacto funcional o patológico en el organismo.

#### Identificación del marco de lectura (ORF)
Dado que las proteínas se leen de tres en tres bases, existen tres posibles marcos de lectura en una hebra simple de ARN. Encontrar el **marco de lectura abierto (ORF)** correcto implica localizar el codón de inicio `AUG` seguido por un fragmento largo sin interrupciones por codones de parada (`UAA`, `UAG`, `UGA`).

#### Análisis Clínico
En la práctica clínica bioinformática, un alineamiento local permite observar mutaciones patógenas:
- Si se encuentra una sustitución missense en un sitio activo enzimático, es muy probable que la proteína pierda su actividad biológica.
- Si ocurre una deleción que altera la pauta de lectura, toda la secuencia de aminoácidos posterior cambiará completamente, generando generalmente una proteína no funcional e inestable.
"""
    }
}


def tutorials_page():
    load_styles()
    top_bar()

    # Si hay un tutorial activo, mostrar su contenido detallado
    active_key = st.session_state.get("active_tutorial")

    if active_key and active_key in TUTORIALS_DATA:
        tutorial = TUTORIALS_DATA[active_key]

        st.markdown(f"<span class='pill'>Nivel: {tutorial['level']}</span>", unsafe_allow_html=True)
        st.title(tutorial["title"])
        st.markdown(f"**Objetivo de aprendizaje:** {tutorial['objective']}")
        st.divider()

        # Renderizar contenido
        st.markdown(tutorial["content"])

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Volver al listado de tutoriales", type="primary", use_container_width=True):
            st.session_state.active_tutorial = None
            st.rerun()

    else:
        st.title("Guías y Tutoriales")
        st.markdown("Ruta de aprendizaje estructurada para comprender las bases de la bioinformática molecular.")

        st.markdown("""
        <style>
        .tutorial-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 200px;
        }
        .tutorial-badge {
            background: #EFF6FF;
            color: #2563EB;
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            width: fit-content;
        }
        .tutorial-title {
            font-size: 18px;
            font-weight: 700;
            color: #0F172A;
            margin-top: 0.75rem;
            margin-bottom: 0.5rem;
        }
        .tutorial-desc {
            font-size: 13.5px;
            color: #475569;
            line-height: 1.5;
            margin-bottom: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)

        # Renderizar cards de tutoriales usando columnas
        keys = list(TUTORIALS_DATA.keys())
        
        # Agrupar en filas de a 2 para que sea responsive y estructurado
        for i in range(0, len(keys), 2):
            col1, col2 = st.columns(2, gap="medium")
            
            with col1:
                key1 = keys[i]
                tut1 = TUTORIALS_DATA[key1]
                st.markdown(f"""
                <div class="tutorial-card">
                    <div>
                        <span class="tutorial-badge">{tut1['level']}</span>
                        <div class="tutorial-title">{tut1['title']}</div>
                        <div class="tutorial-desc">{tut1['desc']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Iniciar lectura", key=f"start_{key1}", use_container_width=True, type="secondary"):
                    st.session_state.active_tutorial = key1
                    new_progress = max(st.session_state.get("progress", 0), 15)
                    st.session_state.progress = new_progress
                    user = st.session_state.get("user", {})
                    if isinstance(user, dict) and "email" in user:
                        from services.progress_service import save_user_progress
                        save_user_progress(
                            user["email"],
                            new_progress,
                            st.session_state.get("streak", 1),
                            st.session_state.get("badges", 0)
                        )
                    st.rerun()
            
            if i + 1 < len(keys):
                with col2:
                    key2 = keys[i+1]
                    tut2 = TUTORIALS_DATA[key2]
                    st.markdown(f"""
                    <div class="tutorial-card">
                        <div>
                            <span class="tutorial-badge">{tut2['level']}</span>
                            <div class="tutorial-title">{tut2['title']}</div>
                            <div class="tutorial-desc">{tut2['desc']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Iniciar lectura", key=f"start_{key2}", use_container_width=True, type="secondary"):
                        st.session_state.active_tutorial = key2
                        new_progress = max(st.session_state.get("progress", 0), 15)
                        st.session_state.progress = new_progress
                        user = st.session_state.get("user", {})
                        if isinstance(user, dict) and "email" in user:
                            from services.progress_service import save_user_progress
                            save_user_progress(
                                user["email"],
                                new_progress,
                                st.session_state.get("streak", 1),
                                st.session_state.get("badges", 0)
                            )
                        st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Volver al inicio", type="secondary", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
