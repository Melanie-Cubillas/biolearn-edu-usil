create extension if not exists pgcrypto;

create table if not exists public.profiles (
    id uuid primary key references auth.users(id) on delete cascade,
    full_name text not null,
    email text unique not null,
    university text not null,
    created_at timestamptz default now()
);

create or replace function public.handle_new_user()
returns trigger as $$
begin
    insert into public.profiles (id, full_name, email, university)
    values (
        new.id,
        coalesce(new.raw_user_meta_data->>'full_name', 'Estudiante'),
        new.email,
        new.raw_user_meta_data->>'university'
    );
    return new;
end;
$$ language plpgsql security definer;

drop trigger if exists on_auth_user_created on auth.users;

create trigger on_auth_user_created
after insert on auth.users
for each row execute function public.handle_new_user();
