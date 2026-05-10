import os

# Telegram
BOT_TOKEN = "8681820401:AAHnSEIm0L2CrgaCKwFolrRCb3FlsqTHWJo"

# Supabase (Возьмите данные в настройках проекта Supabase -> API)
SUPABASE_URL = "https://hyutxxmtkafqvxsbsbcd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh5dXR4eG10a2FmcXZ4c2JzYmNkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg0MDc5MjAsImV4cCI6MjA5Mzk4MzkyMH0.mlxzUeIozH8d4A_66uESAXgKYyzEEbo8lUFZ3otvzMc"

# Модели
VOSK_MODEL_PATH = "model"
LLM_MODEL = "gemma2:9b"

# Параметры обработки
MAX_CHARS_PER_CHUNK = 3500
TEMP_DIR = "temp_audio"

# Создаем папку для временных файлов, если её нет
os.makedirs(TEMP_DIR, exist_ok=True)