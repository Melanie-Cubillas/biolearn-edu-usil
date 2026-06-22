import json
import os

PROGRESS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "progress.json")

def load_user_progress(email: str) -> tuple:
    """Loads the progress, streak, and badges for a given user email from local storage."""
    # Ensure data directory exists
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    
    if not os.path.exists(PROGRESS_FILE):
        return 0, 1, 0  # default progress=0, streak=1, badges=0
        
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        user_data = data.get(email, {})
        progress = user_data.get("progress", 0)
        streak = user_data.get("streak", 1)
        badges = user_data.get("badges", 0)
        return progress, streak, badges
    except Exception:
        return 0, 1, 0

def save_user_progress(email: str, progress: int, streak: int, badges: int):
    """Saves progress, streak, and badges for a given user email to local storage."""
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    
    data = {}
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}
            
    data[email] = {
        "progress": progress,
        "streak": streak,
        "badges": badges
    }
    
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception:
        pass
