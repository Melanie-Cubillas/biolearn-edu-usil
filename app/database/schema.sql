create extension if not exists pgcrypto;

create table if not exists public.profiles (
    id uuid primary key references auth.users(id) on delete cascade,
    full_name text not null,
    email text unique not null,
    university text not null,
    created_at timestamptz default now()
);

create table if not exists public.quizzes (
    id bigint generated always as identity primary key,
    title text not null,
    description text,
    questions_per_attempt integer default 5,
    created_at timestamptz default now()
);

create table if not exists public.quiz_questions (
    id bigint generated always as identity primary key,
    quiz_id bigint not null references public.quizzes(id) on delete cascade,
    question text not null,
    topic text,
    difficulty text default 'Básico',
    explanation text,
    created_at timestamptz default now()
);

create table if not exists public.quiz_options (
    id bigint generated always as identity primary key,
    question_id bigint not null references public.quiz_questions(id) on delete cascade,
    option_text text not null,
    is_correct boolean default false
);

create table if not exists public.quiz_results (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references public.profiles(id) on delete cascade,
    score integer not null,
    total_questions integer not null,
    completed_at timestamptz default now()
);

create table if not exists public.quiz_result_answers (
    id bigint generated always as identity primary key,
    result_id uuid not null references public.quiz_results(id) on delete cascade,
    question_id bigint not null references public.quiz_questions(id),
    selected_option_id bigint not null references public.quiz_options(id),
    is_correct boolean default false
);

create or replace function public.handle_new_user()
returns trigger as $$
begin
    insert into public.profiles (
        id,
        full_name,
        email,
        university
    )
    values (
        new.id,
        coalesce(new.raw_user_meta_data->>'full_name', 'Estudiante'),
        new.email,
        coalesce(new.raw_user_meta_data->>'university', 'No especificada')
    );

    return new;
end;
$$ language plpgsql security definer;

drop trigger if exists on_auth_user_created on auth.users;

create trigger on_auth_user_created
after insert on auth.users
for each row
execute function public.handle_new_user();

alter table public.profiles enable row level security;
alter table public.quizzes enable row level security;
alter table public.quiz_questions enable row level security;
alter table public.quiz_options enable row level security;
alter table public.quiz_results enable row level security;
alter table public.quiz_result_answers enable row level security;

drop policy if exists "read own profile" on public.profiles;
drop policy if exists "update own profile" on public.profiles;
drop policy if exists "read quizzes" on public.quizzes;
drop policy if exists "read quiz questions" on public.quiz_questions;
drop policy if exists "read quiz options" on public.quiz_options;
drop policy if exists "insert own results" on public.quiz_results;
drop policy if exists "read own results" on public.quiz_results;
drop policy if exists "insert own result answers" on public.quiz_result_answers;
drop policy if exists "read own result answers" on public.quiz_result_answers;

create policy "read own profile"
on public.profiles
for select
using (auth.uid() = id);

create policy "update own profile"
on public.profiles
for update
using (auth.uid() = id);

create policy "read quizzes"
on public.quizzes
for select
using (true);

create policy "read quiz questions"
on public.quiz_questions
for select
using (true);

create policy "read quiz options"
on public.quiz_options
for select
using (true);

create policy "insert own results"
on public.quiz_results
for insert
with check (auth.uid() = user_id);

create policy "read own results"
on public.quiz_results
for select
using (auth.uid() = user_id);

create policy "insert own result answers"
on public.quiz_result_answers
for insert
with check (
    exists (
        select 1
        from public.quiz_results qr
        where qr.id = result_id
        and qr.user_id = auth.uid()
    )
);

create policy "read own result answers"
on public.quiz_result_answers
for select
using (
    exists (
        select 1
        from public.quiz_results qr
        where qr.id = result_id
        and qr.user_id = auth.uid()
    )
);

insert into public.quizzes (
    title,
    description,
    questions_per_attempt
)
values (
    'Quiz de Bioinformática',
    'Banco de preguntas sobre ADN, ARN, transcripción, traducción, NCBI, BLAST y mutaciones.',
    5
);

insert into public.quiz_questions (
    quiz_id,
    question,
    topic,
    difficulty,
    explanation
)
values
(1, '¿Qué molécula almacena la información genética?', 'ADN', 'Básico', 'El ADN contiene la información genética hereditaria.'),
(1, '¿Qué significa ADN?', 'ADN', 'Básico', 'ADN significa ácido desoxirribonucleico.'),
(1, '¿Qué bases nitrogenadas forman parte del ADN?', 'ADN', 'Básico', 'El ADN contiene adenina, timina, citosina y guanina.'),
(1, '¿Qué base del ADN se reemplaza por uracilo en el ARN?', 'Transcripción', 'Básico', 'Durante la transcripción, la timina se reemplaza por uracilo.'),
(1, '¿Qué proceso convierte ADN en ARN?', 'Transcripción', 'Básico', 'La transcripción genera ARN a partir de una secuencia de ADN.'),
(1, '¿Qué molécula se produce durante la transcripción?', 'Transcripción', 'Básico', 'La transcripción produce ARN mensajero.'),
(1, '¿Qué representa un codón?', 'Traducción', 'Básico', 'Un codón es un grupo de tres nucleótidos.'),
(1, '¿Cuál es el codón de inicio más común?', 'Traducción', 'Básico', 'AUG es el codón de inicio más común.'),
(1, '¿Qué proceso convierte ARN en proteína?', 'Traducción', 'Básico', 'La traducción interpreta codones del ARN para formar proteínas.'),
(1, '¿Qué es un codón de parada?', 'Traducción', 'Intermedio', 'Un codón de parada indica el fin de la traducción.'),
(1, '¿Qué significa una mutación por sustitución?', 'Mutaciones', 'Intermedio', 'Una sustitución ocurre cuando una base es reemplazada por otra.'),
(1, '¿Qué significa una deleción?', 'Mutaciones', 'Intermedio', 'Una deleción ocurre cuando se pierde una o más bases.'),
(1, '¿Qué significa una inserción?', 'Mutaciones', 'Intermedio', 'Una inserción ocurre cuando se agregan una o más bases.'),
(1, '¿Qué enfermedad está asociada a expansiones CAG en el gen HTT?', 'Huntington', 'Intermedio', 'La enfermedad de Huntington se asocia a expansiones del triplete CAG.'),
(1, '¿Qué gen está relacionado con la enfermedad de Huntington?', 'Huntington', 'Básico', 'El gen HTT está relacionado con la enfermedad de Huntington.'),
(1, '¿Qué gen se relaciona con la anemia falciforme?', 'Anemia falciforme', 'Básico', 'La anemia falciforme está asociada al gen HBB.'),
(1, '¿Qué cambio se asocia comúnmente con anemia falciforme?', 'Anemia falciforme', 'Intermedio', 'Una mutación puntual puede cambiar GAG por GTG en el gen HBB.'),
(1, '¿Qué gen se relaciona con la fibrosis quística?', 'Fibrosis quística', 'Básico', 'La fibrosis quística se asocia al gen CFTR.'),
(1, '¿Qué tipo de mutación puede observarse en fibrosis quística?', 'Fibrosis quística', 'Intermedio', 'Una mutación frecuente en CFTR es una deleción relacionada con F508.'),
(1, '¿Para qué se usa NCBI en BioLearn?', 'NCBI', 'Básico', 'NCBI permite obtener secuencias biológicas reales mediante Accession ID.'),
(1, '¿Qué formato se usa para guardar secuencias descargadas de NCBI?', 'FASTA', 'Básico', 'FASTA es un formato común para almacenar secuencias biológicas.'),
(1, '¿Qué permite comparar un alineamiento tipo BLAST?', 'BLAST', 'Intermedio', 'Permite comparar una secuencia con otra para identificar similitudes y diferencias.'),
(1, '¿Qué indica el porcentaje de identidad en un alineamiento?', 'BLAST', 'Intermedio', 'Indica qué proporción de posiciones coinciden entre dos secuencias alineadas.'),
(1, '¿Qué representa un gap en un alineamiento?', 'BLAST', 'Intermedio', 'Un gap representa una inserción o deleción necesaria para alinear dos secuencias.');

insert into public.quiz_options (
    question_id,
    option_text,
    is_correct
)
values
(1, 'ADN', true), (1, 'ARN', false), (1, 'Proteína', false), (1, 'Glucosa', false),
(2, 'Ácido desoxirribonucleico', true), (2, 'Ácido ribonucleico', false), (2, 'Aminoácido nuclear', false), (2, 'Archivo de datos nucleares', false),
(3, 'Adenina, timina, citosina y guanina', true), (3, 'Adenina, uracilo, citosina y guanina', false), (3, 'Glucosa, timina, calcio y hierro', false), (3, 'Proteína, ARN, ADN y lípido', false),
(4, 'Timina', true), (4, 'Adenina', false), (4, 'Citosina', false), (4, 'Guanina', false),
(5, 'Transcripción', true), (5, 'Traducción', false), (5, 'Deleción', false), (5, 'Alineamiento', false),
(6, 'ARN mensajero', true), (6, 'Proteína', false), (6, 'Glucosa', false), (6, 'Lípido', false),
(7, 'Un grupo de tres nucleótidos', true), (7, 'Una proteína completa', false), (7, 'Una célula', false), (7, 'Un cromosoma completo', false),
(8, 'AUG', true), (8, 'UAA', false), (8, 'UAG', false), (8, 'UGA', false),
(9, 'Traducción', true), (9, 'Transcripción', false), (9, 'Replicación', false), (9, 'Mutación', false),
(10, 'Una señal de finalización de la traducción', true), (10, 'Un inicio de transcripción', false), (10, 'Una base del ADN', false), (10, 'Una enfermedad genética', false),
(11, 'Cambio de una base por otra', true), (11, 'Pérdida de un cromosoma completo', false), (11, 'Duplicación de una célula', false), (11, 'Formación de ARN', false),
(12, 'Pérdida de una o más bases', true), (12, 'Cambio de ARN por proteína', false), (12, 'Aumento de glucosa', false), (12, 'Duplicación de ribosomas', false),
(13, 'Adición de una o más bases', true), (13, 'Eliminación de proteínas', false), (13, 'Cambio de célula', false), (13, 'Formación de lípidos', false),
(14, 'Enfermedad de Huntington', true), (14, 'Fibrosis quística', false), (14, 'Anemia falciforme', false), (14, 'Diabetes tipo 1', false),
(15, 'HTT', true), (15, 'HBB', false), (15, 'CFTR', false), (15, 'BRCA1', false),
(16, 'HBB', true), (16, 'CFTR', false), (16, 'HTT', false), (16, 'TP53', false),
(17, 'GAG a GTG', true), (17, 'CAG a CAGCAGCAG', false), (17, 'Eliminación total del ADN', false), (17, 'Cambio de ARN a glucosa', false),
(18, 'CFTR', true), (18, 'HBB', false), (18, 'HTT', false), (18, 'TP53', false),
(19, 'Deleción', true), (19, 'Transcripción', false), (19, 'Traducción', false), (19, 'Replicación celular', false),
(20, 'Para obtener secuencias biológicas reales', true), (20, 'Para crear contraseñas', false), (20, 'Para diseñar gráficos financieros', false), (20, 'Para comprimir imágenes', false),
(21, 'FASTA', true), (21, 'PDF', false), (21, 'DOCX', false), (21, 'PNG', false),
(22, 'Similitudes y diferencias entre secuencias', true), (22, 'Contraseñas de usuario', false), (22, 'Diseño de interfaces', false), (22, 'Velocidad de internet', false),
(23, 'El porcentaje de coincidencias entre secuencias alineadas', true), (23, 'El número de usuarios registrados', false), (23, 'La longitud de una proteína solamente', false), (23, 'El peso molecular del agua', false),
(24, 'Una separación introducida para alinear secuencias', true), (24, 'Una base nitrogenada', false), (24, 'Un codón de inicio', false), (24, 'Un tipo de proteína', false);