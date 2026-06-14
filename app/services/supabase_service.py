import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if SUPABASE_URL and SUPABASE_ANON_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
else:
    supabase = None


def is_supabase_configured() -> bool:
    return supabase is not None


def get_supabase() -> Client:
    if supabase is None:
        raise ValueError("Supabase no está configurado. Revisa el archivo .env")
    return supabase


def login_user(email: str, password: str) -> dict:
    client = get_supabase()

    response = client.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    return {
        "user": response.user,
        "session": response.session
    }


def register_user(full_name: str, email: str, password: str, university: str) -> dict:
    client = get_supabase()

    response = client.auth.sign_up({
        "email": email,
        "password": password,
        "options": {
            "data": {
                "full_name": full_name,
                "university": university
            }
        }
    })

    return {
        "user": response.user,
        "session": response.session
    }


def get_authenticated_client(access_token: str, refresh_token: str) -> Client:
    client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    client.auth.set_session(access_token, refresh_token)
    return client


def get_profile(user_id: str, access_token: str, refresh_token: str) -> dict:
    client = get_authenticated_client(access_token, refresh_token)

    response = (
        client.table("profiles")
        .select("*")
        .eq("id", user_id)
        .single()
        .execute()
    )

    return response.data


def get_quiz_questions(limit: int = 5) -> list:
    client = get_supabase()

    response = (
        client.table("quiz_questions")
        .select("id, question, topic, difficulty, quiz_options(id, option_text, is_correct)")
        .limit(50)
        .execute()
    )

    questions = response.data or []

    import random
    random.shuffle(questions)

    return questions[:limit]


def save_quiz_result(
    user_id: str,
    score: int,
    total_questions: int,
    access_token: str,
    refresh_token: str
):
    client = get_authenticated_client(access_token, refresh_token)

    response = (
        client.table("quiz_results")
        .insert({
            "user_id": user_id,
            "score": score,
            "total_questions": total_questions
        })
        .execute()
    )

    return response.data
