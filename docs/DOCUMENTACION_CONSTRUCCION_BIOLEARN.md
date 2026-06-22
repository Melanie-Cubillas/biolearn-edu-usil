# Documentación técnica para la construcción de BioLearn desde cero

## 1. Descripción general del proyecto

BioLearn es una plataforma web interactiva y educativa diseñada para estudiantes universitarios, orientada al aprendizaje práctico de la bioinformática y la biología molecular genética. El sistema resuelve la brecha de comprensión en procesos de flujo genético (como transcripción de ADN a ARN y traducción de ARN a proteínas) y reconocimiento de mutaciones clínicas patológicas asociadas a enfermedades hereditarias reales (Huntington, anemia falciforme y fibrosis quística). BioLearn combina simuladores interactivos con bases de datos públicas (NCBI), permitiendo que conceptos abstractos se experimenten mediante datos moleculares reales en un entorno web intuitivo y de alto rendimiento.

## 2. Objetivo de la documentación

Esta guía técnica tiene como finalidad describir detalladamente la arquitectura, dependencias, configuración de servicios, estructuración de archivos, lógicas de análisis bioinformático y criterios de diseño frontend para construir y desplegar la plataforma BioLearn desde cero. Sirve como manual de reconstrucción para desarrolladores y administradores del sistema, garantizando la consistencia y escalabilidad de la base del código.

## 3. Tecnologías utilizadas

El proyecto está construido sobre las siguientes tecnologías y librerías de Python:

| Tecnología | Función principal en el proyecto |
| :--- | :--- |
| **Python** | Lenguaje de programación base para la lógica bioinformática y del servidor. |
| **Streamlit** | Framework web utilizado para renderizar la interfaz de usuario reactiva en tiempo real. |
| **Supabase** | Base de datos relacional (PostgreSQL) y servicio de autenticación de usuarios (Supabase Auth). |
| **Biopython** | Librería especializada para el manejo de estructuras biológicas, complementariedad, traducción y consultas a NCBI. |
| **Pandas** | Manipulación y estructuración de tablas de codones y alineamientos de mutaciones en DataFrames. |
| **Plotly** | Renderización de gráficos y métricas del progreso y resultados de evaluaciones. |
| **python-dotenv** | Carga de variables de entorno para las claves API y conexiones de base de datos desde un archivo local `.env`. |
| **Git y GitHub** | Control de versiones del software y almacenamiento del repositorio de código. |

## 4. Requisitos previos

Antes de iniciar la construcción de la aplicación, el desarrollador debe contar con:

* **Python 3.9 o superior** instalado en el sistema local.
* **Git** instalado para el clonado y versionamiento de código.
* **Visual Studio Code** u otro editor de texto adecuado para desarrollo en Python.
* **Cuenta activa en GitHub** para hospedar el repositorio.
* **Proyecto creado en Supabase** con credenciales de acceso disponibles.
* **Conexión estable a Internet** para la instalación de dependencias y pruebas con APIs.
* **Conocimientos en:** Sintaxis de Python, fundamentos de bases de datos PostgreSQL, conceptos básicos de biología molecular (ADN, ARN, codones y mutaciones) y manejo de terminal de comandos.

## 5. Creación del proyecto desde cero

Para crear el espacio de trabajo inicial, ejecuta los siguientes comandos en la terminal de tu sistema operativo:

```bash
mkdir biolearn-edu-usil
cd biolearn-edu-usil
git init
```

## 6. Estructura recomendada del proyecto

El proyecto BioLearn se organiza siguiendo un patrón de desacoplamiento entre componentes visuales, servicios y páginas:

```text
biolearn-edu-usil/
├── .streamlit/
│   └── config.toml
├── app/
│   ├── main.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── cards.py
│   │   └── layout.py
│   ├── data/
│   │   ├── fasta/
│   │   └── progress.json
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── dashboard.py
│   │   ├── disease_detail.py
│   │   ├── diseases.py
│   │   ├── login.py
│   │   ├── mutation_recognition.py
│   │   ├── quiz.py
│   │   ├── register.py
│   │   ├── transcription.py
│   │   ├── translation.py
│   │   └── tutorials.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── bioinformatics_service.py
│   │   ├── blast_service.py
│   │   ├── ncbi_service.py
│   │   ├── progress_service.py
│   │   └── supabase_service.py
│   └── requirements.txt
├── docs/
│   └── DOCUMENTACION_CONSTRUCCION_BIOLEARN.md
├── .env.example
├── .gitignore
└── README.md
```

### Descripción de carpetas y archivos principales

| Carpeta / Archivo | Propósito |
| :--- | :--- |
| **.streamlit/** | Configuración del tema visual de Streamlit (colores de la marca, visualización del menú lateral). |
| **app/** | Código fuente ejecutable de la aplicación de Streamlit. |
| [app/main.py](file:///e:/UNIVERSIDAD/2026-1/Bioinformatica/app-bio/biolearn-edu-usil/app/main.py) | Punto de entrada principal y controlador de rutas de la aplicación. |
| **app/components/** | Componentes de la interfaz reutilizables como headers y hojas de estilo base. |
| **app/data/** | Directorio para archivos FASTA cacheados (`fasta/`) y almacenamiento local del progreso del alumno (`progress.json`). |
| **app/pages/** | Vistas independientes que representan las páginas o módulos del sistema. |
| **app/services/** | Módulos con lógica pura (bioinformática, alineamiento local, llamadas API, persistencia). |
| [app/requirements.txt](file:///e:/UNIVERSIDAD/2026-1/Bioinformatica/app-bio/biolearn-edu-usil/app/requirements.txt) | Listado de librerías y dependencias necesarias para ejecutar el proyecto. |
| **.env.example** | Plantilla que indica las variables de entorno necesarias para la aplicación sin credenciales reales expuestas. |
| **.gitignore** | Archivo para evitar la subida a Git de entornos virtuales, cachés y archivos con credenciales secretas. |

## 7. Configuración del entorno virtual

Para evitar conflictos de librerías, se debe aislar el entorno en un ambiente virtual. Ejecuta los siguientes comandos (ejemplo para Windows):

```bash
python -m venv venv
venv\Scripts\activate
```

*Nota para sistemas basados en Unix (Linux / macOS):* El comando para activar el entorno es: `source venv/bin/activate`.

## 8. Instalación de dependencias

Con el entorno virtual activado, instala las librerías necesarias especificadas en el archivo de requerimientos:

```bash
pip install -r app/requirements.txt
```

Si estás construyendo el proyecto desde cero y has instalado librerías adicionales, puedes exportar tu archivo `requirements.txt` ejecutando:

```bash
pip freeze > app/requirements.txt
```

## 9. Variables de entorno

Crea un archivo `.env` en la raíz del proyecto para almacenar de manera segura las llaves secretas. Ejemplo del archivo `.env`:

```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=tu-anon-key-de-supabase
NCBI_EMAIL=tu_correo@usil.pe
```

**Seguridad:** Asegúrate de no subir jamás el archivo `.env` a repositorios públicos. Genera siempre un `.env.example` limpio con variables vacías para otros desarrolladores.

## 10. Archivo .gitignore

Asegúrate de incluir en el archivo `.gitignore` los directorios temporales, archivos de configuración local y dependencias:

```gitignore
.env
venv/
__pycache__/
*.pyc
.pytest_cache/
.DS_Store
app/data/fasta/*.fasta
app/data/progress.json
```

## 11. Configuración de Supabase

Supabase provee la autenticación y la base de datos relacional para BioLearn. Sigue estos pasos para configurarlo:

1. **Crear Proyecto:** Inicia un nuevo proyecto en la consola de Supabase.
2. **Obtener Credenciales:** Copia la URL del proyecto (`SUPABASE_URL`) y la Anon Key de la API pública (`SUPABASE_ANON_KEY`) e inyéctalas en tu archivo `.env`.
3. **Configurar Autenticación:** Habilita el inicio de sesión con Email y Contraseña desde el panel de Supabase Auth.
4. **Estructura de Tablas:** Ejecuta las siguientes consultas DDL en el editor SQL de Supabase y observa su diseño en tablas Markdown:

### Tabla: `profiles`

Almacena la información académica básica del estudiante creada al registrarse.

```sql
create table profiles (
  id uuid references auth.users not null primary key,
  full_name text,
  university text,
  updated_at timestamp with time zone default timezone('utc'::text, now())
);
```

| Columna | Tipo de Datos | Restricciones | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `uuid` | `PRIMARY KEY`, `REFERENCES auth.users` | Identificador único del usuario vinculado a Supabase Auth. |
| `full_name` | `text` | - | Nombre completo del estudiante. |
| `university` | `text` | - | Institución universitaria del estudiante. |
| `updated_at` | `timestamp with time zone` | `DEFAULT now()` | Fecha de última actualización del perfil. |

---

### Tabla: `quiz_questions`

Banco de preguntas dinámicas cargadas en las evaluaciones de BioLearn.

```sql
create table quiz_questions (
  id bigint generated by default as identity primary key,
  question text not null,
  topic text not null,
  difficulty text not null,
  explanation text,
  created_at timestamp with time zone default timezone('utc'::text, now())
);
```

| Columna | Tipo de Datos | Restricciones | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `bigint` | `PRIMARY KEY`, `GENERATED BY DEFAULT AS` | Identificador único autoincremental de la pregunta. |
| `question` | `text` | `NOT NULL` | Enunciado o texto de la pregunta académica. |
| `topic` | `text` | `NOT NULL` | Tema evaluado (ej. ADN, ARN, Transcripción). |
| `difficulty` | `text` | `NOT NULL` | Nivel de dificultad asignado (Básico, Intermedio, Avanzado). |
| `explanation` | `text` | - | Explicación teórica revelada después de enviar la respuesta. |
| `created_at` | `timestamp with time zone` | `DEFAULT now()` | Fecha de creación del registro. |

---

### Tabla: `quiz_options`

Opciones de respuesta para las preguntas del quiz.

```sql
create table quiz_options (
  id bigint generated by default as identity primary key,
  question_id bigint references quiz_questions(id) on delete cascade,
  option_text text not null,
  is_correct boolean default false
);
```

| Columna | Tipo de Datos | Restricciones | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `bigint` | `PRIMARY KEY`, `GENERATED BY DEFAULT AS` | Identificador único autoincremental de la opción. |
| `question_id` | `bigint` | `REFERENCES quiz_questions(id) ON DELETE CASCADE` | Llave foránea vinculada a la pregunta correspondiente. |
| `option_text` | `text` | `NOT NULL` | Texto visible de la opción. |
| `is_correct` | `boolean` | `DEFAULT false` | Bandera booleana que define si es la alternativa correcta. |

---

### Tabla: `quiz_results`

Historial de resultados guardados por cada estudiante tras resolver la autoevaluación.

```sql
create table quiz_results (
  id bigint generated by default as identity primary key,
  user_id uuid references auth.users,
  score integer not null,
  total_questions integer not null,
  created_at timestamp with time zone default timezone('utc'::text, now())
);
```

| Columna | Tipo de Datos | Restricciones | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `bigint` | `PRIMARY KEY`, `GENERATED BY DEFAULT AS` | Identificador único de la sesión del quiz completada. |
| `user_id` | `uuid` | `REFERENCES auth.users` | Identificador del estudiante que completó la prueba. |
| `score` | `integer` | `NOT NULL` | Cantidad de aciertos del usuario. |
| `total_questions` | `integer` | `NOT NULL` | Número total de preguntas evaluadas en la sesión. |
| `created_at` | `timestamp with time zone` | `DEFAULT now()` | Fecha y hora de realización. |

## 12. Punto de entrada de la aplicación

El archivo principal [app/main.py](file:///e:/UNIVERSIDAD/2026-1/Bioinformatica/app-bio/biolearn-edu-usil/app/main.py) inicializa el framework de Streamlit, define configuraciones como el título de la página, icono, layout y oculta los menús nativos y barra lateral automática de Streamlit para proveer una UI personalizada. Controla en tiempo real qué página se debe renderizar basándose en el estado de sesión `st.session_state.page`.

### Ejemplo conceptual de inicialización y enrutamiento en BioLearn:

```python
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

# Configuración inicial de Streamlit
st.set_page_config(
    page_title="BioLearn Edu",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicialización de estados de sesión básicos
if "page" not in st.session_state:
    st.session_state.page = "login"
if "user" not in st.session_state:
    st.session_state.user = None
if "selected_disease" not in st.session_state:
    st.session_state.selected_disease = "huntington"

# Directorio de rutas de la aplicación
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

# Renderizar la página actual según el estado de la sesión
current_page_fn = pages.get(st.session_state.page, login_page)
current_page_fn()
```

## 13. Componentes reutilizables

Ubicados en el directorio `app/components/`:

### [app/components/layout.py](file:///e:/UNIVERSIDAD/2026-1/Bioinformatica/app-bio/biolearn-edu-usil/app/components/layout.py)
* **`load_styles()`**: Carga tipografías externas (Outfit de Google Fonts) e inyecta reglas CSS globales para normalizar el diseño, forzar fondos claros degradados, forzar textos legibles, definir tarjetas de diseño SaaS y normalizar la altura de botones e inputs a `40px` de forma homogénea con bordes de `10px` y sombras suaves.
* **`brand_logo()`**: Renderiza el logotipo de la marca (`BioLearn`) de forma consistente con degradado e identidad visual tecnológica y sin emoticones.
* **`top_bar()`**: Renderiza la barra de navegación superior utilizando columnas de Streamlit `Inicio | Quiz | Tutoriales` e inyecta el nombre del usuario conectado en la esquina superior derecha. Determina dinámicamente qué botón mostrar en estado activo (`type="primary"`) y cuáles en pasivo (`type="secondary"`) según el valor en `st.session_state.page`.

### [app/components/cards.py](file:///e:/UNIVERSIDAD/2026-1/Bioinformatica/app-bio/biolearn-edu-usil/app/components/cards.py)
* **`option_card(title, description, button_text, target_page)`**: Renderiza un contenedor genérico con borde `st.container(border=True)`, inyecta un encabezado markdown, un texto descriptivo y expone un botón de redirección de ancho completo. Al pulsarse, actualiza `st.session_state.page` al valor de `target_page` y ejecuta un refresco mediante `st.rerun()`.

## 14. Servicios del proyecto

Ubicados en el directorio `app/services/`:

* **[supabase_service.py](file:///e:/UNIVERSIDAD/2026-1/Bioinformatica/app-bio/biolearn-edu-usil/app/services/supabase_service.py)**: Responsable de la comunicación directa con el SDK de Supabase. Expone funciones para el inicio de sesión (`login_user`), obtención del perfil del estudiante (`get_profile`), recuperación de preguntas de autoevaluación (`get_quiz_questions`), persistencia de puntajes del quiz (`save_quiz_result`) e inicio del flujo de recuperación de claves (`reset_password`).
* **[ncbi_service.py](file:///e:/UNIVERSIDAD/2026-1/Bioinformatica/app-bio/biolearn-edu-usil/app/services/ncbi_service.py)**: Responsable del contacto con las bases de datos de NCBI mediante Biopython Entrez. Limpia el Accession ID, busca las secuencias en GenBank, descarga la secuencia en formato FASTA y la parsea. Además, gestiona un sistema de caché local escribiendo y leyendo archivos en la ruta `app/data/fasta/` para evitar descargar archivos duplicados.
* **[bioinformatics_service.py](file:///e:/UNIVERSIDAD/2026-1/Bioinformatica/app-bio/biolearn-edu-usil/app/services/bioinformatics_service.py)**: Procesa lógicas biológicas puras. Limpia secuencias (`clean_sequence`), filtra nucleótidos válidos de ADN (`keep_valid_dna`), realiza transcripción de ADN a ARN mensajero reemplazando nucleótidos T por U (`transcribe_dna_to_rna`), detecta la posición de codones de parada (`find_stop_codons`) y traduce codón por codón a aminoácidos deteniéndose en caso de codón de parada (`translate_dna_to_protein`).
* **[blast_service.py](file:///e:/UNIVERSIDAD/2026-1/Bioinformatica/app-bio/biolearn-edu-usil/app/services/blast_service.py)**: Implementa el alineamiento global Needleman-Wunsch para comparar dos secuencias de nucleótidos base por base. Computa métricas de alineamiento (Identidad, Gaps, Matches, Mismatches), clasifica las mutaciones puntuales detectadas en Sustitución, Inserción y Deleción, y evalúa patrones clínicos predefinidos según el gen seleccionado.
* **[progress_service.py](file:///e:/UNIVERSIDAD/2026-1/Bioinformatica/app-bio/biolearn-edu-usil/app/services/progress_service.py)**: Carga y guarda localmente en el archivo [app/data/progress.json](file:///e:/UNIVERSIDAD/2026-1/Bioinformatica/app-bio/biolearn-edu-usil/app/data/progress.json) el progreso global (`progress`), la racha activa de estudio (`streak`) y la cantidad de insignias del quiz (`badges`) de los estudiantes indexándolos bajo su correo electrónico institucional.

## 15. Construcción del login y registro

### Login
* **Interfaz:** Los campos `st.text_input` para correo institucional y contraseña, así como el botón de ingreso, registro y "¿Olvidaste tu contraseña?" están encapsulados en un contenedor visual tipo tarjeta mediante `with st.container(border=True)`.
* **Recuperación:** Cuando el estado `st.session_state.forgot_password` se activa, la interfaz cambia al modo de recuperación. Solicita el correo institucional y expone el botón "Enviar instrucciones", el cual ejecuta la llamada a `reset_password` del servicio de Supabase.
* **Sesión:** Al ingresar credenciales correctas, el servicio valida la autenticidad en Supabase. Si tiene éxito, se obtienen los datos de la tabla `profiles` mediante `get_profile()`. El usuario se guarda en `st.session_state.user`, se carga su progreso local mediante el `progress_service` y se le redirige al Dashboard.

### Registro
* **Campos:** Requiere Nombre completo, Correo institucional, Universidad, Contraseña y Confirmar contraseña.
* **Validación frontend:** Comprueba que no existan campos vacíos y que el correo cumpla la expresión de dominio académico (terminación `.edu`, `.edu.pe` o `usil.pe`).
* **Validación de contraseñas:** Valida en frontend que la contraseña y confirmación sean idénticas. Si se cumplen los requisitos previos, se llama a `supabase.auth.sign_up` adjuntando metadatos para guardar el perfil del usuario. Al registrarse, se le redirige inmediatamente a la pantalla de Login.

## 16. Construcción del layout y navegación

La navegación principal de los usuarios registrados es controlada por el componente `top_bar` en el Header:
* **Botón Inicio:** Redirige al panel general (`dashboard`).
* **Botón Quiz:** Abre el panel de autoevaluación (`quiz`).
* **Botón Tutoriales:** Abre el portal de guías prácticas (`tutorials`).

La redirección hacia los simuladores científicos especializados se maneja directamente desde las tarjetas de acción del Dashboard o desde las secciones internas del detalle de enfermedades genéticas (`disease_detail`). La navegación secundaria o de regreso utiliza botones del tipo `secondary` llamando a `st.rerun()`.

## 17. Construcción del módulo de Inicio

El dashboard principal se compone de:
* **Tarjeta de bienvenida:** Contenedor superior con estilo degradado que saluda al estudiante con su nombre y despliega sus estadísticas de aprendizaje recuperadas del estado de sesión: progreso en porcentaje, racha en días e insignias acumuladas.
* **Sección de Módulos de Análisis:** Tres columnas dedicadas a iniciar directamente los simuladores de Transcripción de ADN, Traducción de Proteínas y Reconocimiento de Mutaciones.
* **Sección de Recursos y Autoevaluación:** Tres columnas destinadas a abrir la Base de Enfermedades, el Quiz Académico y el listado de Guías/Tutoriales.
* **Actividad reciente:** Contenedor visual izquierdo que muestra los hitos logrados por el usuario durante el día actual.
* **Próximo objetivo:** Contenedor derecho que calcula de manera predictiva la meta formativa sugerida basada en su porcentaje de progreso y lo plasma en una barra de progreso lineal de color azul y violeta.
* **Cerrar sesión:** Botón inferior que persiste el progreso actual en `progress.json`, limpia el estado de sesión del usuario y redirige a la pantalla de Login.

## 18. Construcción del módulo de Transcripción

* **Entrada:** Caja de texto `st.text_area` que carga por defecto la secuencia de referencia del caso de estudio activo en la sesión. Permite al estudiante editarla libremente.
* **Proceso:** Llama a `transcribe_dna_to_rna` en el servicio bioinformático. Limpia la secuencia, filtra las bases nitrogenadas no válidas (conservando A, T, C, G y N) y reemplaza las Timinas (T) por Uracilos (U).
* **Ejemplo simple:**
  * ADN: `ATGCGT`
  * ARN: `AUGCGU`
* **Resultado:** Imprime la secuencia de ADN depurada y el ARN mensajero en bloques de código (`st.code`).
* **Explicación educativa:** Despliega una lista con la resolución paso a paso explicada didácticamente. Busca en el ARN generado codones de parada (`UAA`, `UAG`, `UGA`) y los visualiza en una tabla interactiva con sus índices de base correspondientes.

## 19. Construcción del módulo de Traducción

* **Entrada:** Secuencia de ADN/ARN proporcionada por el usuario o cargada por el caso de estudio correspondiente en la base de enfermedades.
* **Proceso:** Invoca a `translate_dna_to_protein` en el servicio bioinformático. Convierte la entrada a mayúsculas, genera el ARN mensajero y realiza la lectura por codones (bloques contiguos de tres nucleótidos). Traduce cada codón a su aminoácido correspondiente y detiene el proceso si detecta un codón de parada.
* **Resultado:** Despliega el ARN mensajero generado, la cadena de codones delimitada por plepas (`|`) y la secuencia de proteína resultante en bloques de código.
* **Explicación educativa:** Imprime una tabla detallada con las columnas del mapeo: codón ARN, codón ADN equivalente y aminoácido asociado. Presenta una tabla con las posiciones de codones de parada identificados y la resolución paso a paso del proceso celular simulado.

## 20. Construcción del módulo de Mutaciones

* **Entrada:** Requiere la secuencia referencial de ADN y la secuencia mutada o del paciente obtenida del caso clínico.
* **Proceso:** Llama a `detect_mutations` en el servicio de blast. Ejecuta el alineamiento global Needleman-Wunsch para comparar las hebras nucleótido a nucleótido.
* **Mutaciones identificadas:**
  * **Sustitución:** Compara las bases alineadas y detecta diferencias de nucleótidos entre hebras.
  * **Inserción:** Detecta bases en la hebra mutada que corresponden a un gap (`-`) en la referencia.
  * **Deleción:** Detecta gaps (`-`) en la hebra mutada correspondientes a una base en la referencia.
* **Visualización:**
  * Bloques métricos interactivos que detallan porcentaje de identidad, coincidencias, diferencias y gaps.
  * Tres bloques de código paralelos que emulan la vista tradicional de alineamientos tipo BLAST (Referencia alineada, línea de coincidencia `|` o diferencia `*`, y secuencia mutada alineada).
  * Tabla interactiva que detalla tipo de mutación (Sustitución, Inserción, Deleción), posición y bases involucradas.
  * Bloque de advertencia que indica el diagnóstico y la interpretación molecular según el gen de la enfermedad seleccionada.

## 21. Modo exploratorio NCBI

Para garantizar un entorno educativo controlado y seguro en la aplicación:
* **Frontend:** La opción "Modo exploratorio" o "Buscar en NCBI" se muestra explícitamente deshabilitada en la interfaz mediante botones inactivos con borde discontinuo, tipografía gris claro y la leyenda "(Disponible próximamente)".
* **Seguridad de datos expuestos:**
  * **Datos válidos a mostrar:** Accession ID de la consulta, Nombre o descripción científica del gen, Longitud de la secuencia en pares de bases (pb) y la Fuente de origen del dato.
  * **Datos prohibidos:** Rutas locales del sistema de archivos del servidor (ej. `/app/data/fasta/NM_...`), pasos de lectura/escritura en disco o llamadas internas de depuración del servidor.

## 22. Construcción del Quiz

* **Carga de preguntas:** Consume dinámicamente cinco preguntas del banco en Supabase mediante `get_quiz_questions`. Las opciones de respuesta se mezclan de forma aleatoria para evitar patrones fijos.
* **Estado inicial:** Los elementos de radio-button de Streamlit `st.radio` se configuran con el parámetro `index=None` para forzar que ninguna opción esté preseleccionada.
* **Validación visual:** Al pulsar "Enviar respuestas", se valida en el frontend que no queden preguntas sin responder. Si hay pendientes, se despliega una advertencia indicando los números de pregunta faltantes.
* **Post-envío:** Tras el envío, los radio-buttons se deshabilitan. El sistema pinta un mensaje de éxito (`st.success`) si la opción elegida es correcta o un error (`st.error`) con la alternativa correcta si falló. Despliega un bloque markdown con la explicación científica de la respuesta y registra el puntaje obtenido del estudiante en Supabase mediante `save_quiz_result`.

## 23. Construcción de Tutoriales

El módulo de tutoriales se implementa en forma de una ruta de aprendizaje interactiva con cuadrículas de tarjetas académicas.

### Detalle de la Ruta de Aprendizaje (8 Guías)

1. **Introducción a la Bioinformática**
   * **Descripción:** Conceptos base de la bioinformática y su fusión de biología y ciencias de la computación.
   * **Objetivo de aprendizaje:** Comprender el rol de la bioinformática en la recopilación y análisis de grandes datos genómicos.
   * **Nivel sugerido:** Básico.

2. **Conceptos Básicos: ADN, ARN y Proteínas**
   * **Descripción:** Flujo de información genética molecular y Dogma Central de la Biología.
   * **Objetivo de aprendizaje:** Identificar diferencias estructurales y bases nitrogenadas de ácidos nucleicos y proteínas.
   * **Nivel sugerido:** Básico.

3. **Transcripción: Del ADN al ARN**
   * **Descripción:** Mecanismo celular de copia de una hebra molde de ADN a ARN mensajero.
   * **Objetivo de aprendizaje:** Aplicar reglas de complementariedad y reconocer la polaridad de las secuencias.
   * **Nivel sugerido:** Básico.

4. **Traducción: Síntesis de Proteínas**
   * **Descripción:** Mecanismo de decodificación del ARNm en codones para sintetizar aminoácidos.
   * **Objetivo de aprendizaje:** Utilizar la tabla del código genético estándar y detectar codones de inicio y parada.
   * **Nivel sugerido:** Intermedio.

5. **Mutaciones Genéticas y sus Tipos**
   * **Descripción:** Alteraciones de nucleótidos y clasificación en sustituciones, inserciones y deleciones.
   * **Objetivo de aprendizaje:** Distinguir efectos de mutaciones silenciosas, missense y nonsense en proteínas.
   * **Nivel sugerido:** Intermedio.

6. **Secuencias y Formato FASTA**
   * **Descripción:** Estructura y almacenamiento computacional estándar de datos biológicos.
   * **Objetivo de aprendizaje:** Estructurar y leer cabeceras y secuencias en archivos de texto plano.
   * **Nivel sugerido:** Básico.

7. **Uso de Bases de Datos NCBI y GenBank**
   * **Descripción:** Exploración y uso del centro nacional de biotecnología y uso de identificadores.
   * **Objetivo de aprendizaje:** Buscar genes específicos e interpretar de forma correcta un Accession ID.
   * **Nivel sugerido:** Intermedio.

8. **Interpretación Biológica de Secuencias**
   * **Descripción:** Análisis bioinformático final de variantes moleculares y su impacto en patologías clínicas.
   * **Objetivo de aprendizaje:** Deducir el impacto de sustituciones y cambios de pauta en marcos de lectura abiertos (ORF).
   * **Nivel sugerido:** Avanzado.

*Navegación:* Al seleccionar un tema, la interfaz oculta la cuadrícula de tutoriales y despliega el lector interactivo con el contenido markdown formateado y un botón prominente para volver al menú de guías.

## 24. Diseño visual y criterios frontend

El frontend de BioLearn sigue criterios estrictos de diseño para proyectar una apariencia profesional, moderna y académica:

* **Paleta de Colores:** Uso restringido de tonos de la marca (azul, celeste, índigo, violeta, blanco y grises neutros). Quedan descartados colores estridentes.
* **Componentes visuales:** Tarjetas modernas (estilo glassmorphism) con esquinas redondeadas (`10px` o `20px` según el elemento) y sombras muy suaves (`box-shadow: 0 4px 15px rgba(15,23,42,0.03)`) para asegurar el contraste.
* **Cero Emojis:** Queda prohibido el uso de emojis dentro de la plataforma (títulos, menús, botones, leyendas). Para la categorización visual se utilizan siglas de texto estilizadas (`TRN`, `TRD`, `MUT`) y figuras coloreadas mediante estilos CSS puros.
* **Responsividad:** Implementación de columnas dinámicas de Streamlit y contenedores flexibles que se adaptan a resoluciones de dispositivos móviles, tabletas y computadoras de escritorio.

## 25. Ejecución local del proyecto

Para desplegar y ejecutar BioLearn en un entorno local de desarrollo, siga los siguientes pasos:

```bash
# 1. Clonar el repositorio
git clone https://github.com/Melanie-Cubillas/biolearn-edu-usil.git
cd biolearn-edu-usil

# 2. Crear y activar el entorno virtual en Windows
python -m venv venv
venv\Scripts\activate

# 3. Instalar librerías del proyecto
pip install -r app/requirements.txt

# 4. Configurar variables de entorno locales
# Duplica el archivo de plantilla y configúralo con tus credenciales de Supabase
cp .env.example .env

# 5. Iniciar la aplicación
streamlit run app/main.py
```

## 26. Pruebas técnicas

La integridad técnica del proyecto se valida mediante la ejecución de la siguiente matriz de pruebas funcionales:

| Prueba | Acciones a realizar | Resultado esperado |
| :--- | :--- | :--- |
| **Ejecutar Streamlit** | Correr `streamlit run app/main.py` | La app levanta localmente sin excepciones en consola y abre el puerto 8501. |
| **Login** | Introducir credenciales reales y pulsar ingresar | El formulario se conecta a Supabase Auth, carga el perfil y redirige al dashboard. |
| **Navegación** | Clic en botones del header de navegación | Redirección inmediata entre Inicio, Quiz y Tutoriales con indicador de botón activo. |
| **Transcripción** | Ingresar secuencia de ADN y transcribir | Devuelve secuencia de ARN mensajero, codones de parada correctos y pasos lógicos. |
| **Traducción** | Traducir secuencia de ADN a proteína | Genera el ARN mensajero, tabla de codones de aminoácidos y cadena polipeptídica final. |
| **Mutaciones** | Alinear dos secuencias en el simulador | Muestra porcentaje de identidad, alineamiento tipo BLAST y tabla de mutaciones clasificadas. |
| **Quiz** | Iniciar quiz académico | Las preguntas cargan con alternativas mezcladas y los radio-buttons inician vacíos. |
| **Tutoriales** | Abrir sección de guías y seleccionar un tema | Abre el lector de contenido markdown interactivo del tema respectivo sin errores. |

## 27. Control de versiones

Para realizar desarrollos e incorporar mejoras al proyecto, se debe seguir la metodología de Git Flow recomendada:

```bash
# Crear una nueva rama para la mejora
git switch -c feature/cambios

# Agregar los archivos modificados
git add .

# Generar un commit claro con nomenclatura estándar
git commit -m "feat: implementar lógica de persistencia local de progreso de estudiantes"

# Subir la rama local al repositorio de GitHub
git push -u origin feature/cambios
```

## 28. Consideraciones de seguridad

* **Exclusión de Secretos:** El archivo `.env` nunca debe subirse al control de versiones de Git. El archivo `.gitignore` debe excluir explícitamente el `.env` y el directorio `venv/`.
* **Manejo de Errores:** Evita exponer trazas del sistema (stack traces) de Python o errores HTTP nativos de Supabase al estudiante; utiliza bloques `try-except` para renderizar avisos de error comprensibles y amigables.
* **Ocultar Datos Críticos:** Las rutas absolutas del servidor local no deben ser accesibles en las vistas del frontend.
* **Integridad de las Evaluaciones:** La identificación de respuestas correctas del quiz no debe enviarse al cliente en las opciones HTML antes de que el usuario envíe su evaluación para calificar.

## 29. Limitaciones técnicas

* **Enfoque Académico:** BioLearn es una herramienta educativa universitaria orientada al aprendizaje simulado. No reemplaza herramientas bioinformáticas clínicas ni profesionales.
* **Algoritmos Nativos:** El alineamiento global Needleman-Wunsch implementado de forma secuencial y en Python nativo posee complejidad de procesamiento lineal; no es óptimo para secuencias masivas de millones de bases.
* **Dependencia Externa:** El sistema de inicio de sesión y la base de datos de preguntas dependen enteramente del estado en línea de la API de Supabase.

## 30. Mejoras futuras

* **Recuperación real conectada:** Implementar un flujo completo de redirección a landing de cambio de clave al pulsar el enlace del correo de recuperación.
* **Progreso persistente en BD:** Reemplazar el almacenamiento local actual en formato JSON por una tabla de progreso vinculada a Supabase para sincronización multiplataforma.
* **Mayor volumen de Casos:** Añadir más casos de estudio genéticos moleculares y enfermedades asociadas.
* **Visualizador 3D:** Integrar visores interactivos en 3D de estructuras tridimensionales de proteínas.
* **Exportación:** Permitir al estudiante descargar reportes en formato PDF con los resultados de sus simulaciones y alineamientos de mutaciones.
