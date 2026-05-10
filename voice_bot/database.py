from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_to_storage(file_path: str, file_name: str) -> str:
    """Загружает аудио в Supabase Storage и возвращает публичную ссылку"""
    with open(file_path, 'rb') as f:
        supabase.storage.from_("voice-notes").upload(file_name, f)
    return supabase.storage.from_("voice-notes").get_public_url(file_name)

def save_note_to_db(user_id: int, title: str, raw_text: str, summary: str, tags: list, file_url: str):
    """Сохраняет структурированную заметку в таблицу notes"""
    data = {
        "user_id": user_id,
        "title": title,
        "raw_text": raw_text,
        "summary": summary,
        "tags": tags,
        "file_url": file_url
    }
    return supabase.table("notes").insert(data).execute()

def fetch_notes(user_id: int):
    """Получает все заметки пользователя для веб-интерфейса"""
    return supabase.table("notes").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()