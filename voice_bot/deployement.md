# 🚀 Инструкция по развертыванию Smart Voice Notes

Система для создания интеллектуальных заметок из голосовых сообщений. 
**Стек:** Telegram (aiogram), Vosk (STT), Gemma 2 9b (Ollama), Supabase (DB/Storage), Streamlit (Web).

## 📋 Требования к системе
- **ОС:** Linux (Ubuntu рекомендуемо), macOS или Windows.
- **RAM:** Минимум 16 ГБ (Gemma 2 9b требует ~10 ГБ, Vosk ~2 ГБ).
- **Библиотеки:** Установленный `FFmpeg` в системе.

## 🛠 Шаг 1: Установка системных зависимостей

### Linux (Ubuntu):
```bash
sudo apt update
sudo apt install ffmpeg python3-venv wget unzip

macOS:
code Bash

brew install ffmpeg

📦 Шаг 2: Настройка проекта и окружения

    Клонируйте репозиторий и создайте виртуальное окружение:

code Bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

    Создайте файл .env в корне проекта и заполните его:

code Env

BOT_TOKEN=ваш_токен_телеграм
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

🎙 Шаг 3: Установка моделей
Vosk (STT):

Скачайте большую русскую модель и распакуйте её в папку model:
code Bash

wget https://alphacephei.com/vosk/models/vosk-model-ru-0.42.zip
unzip vosk-model-ru-0.42.zip
mv vosk-model-ru-0.42 model
rm vosk-model-ru-0.42.zip

Ollama (LLM):

Установите Ollama и скачайте модель:
code Bash

ollama pull gemma2:9b

☁️ Шаг 4: Настройка Supabase

    SQL Editor: Создайте таблицу notes:

code SQL

CREATE TABLE notes (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id bigint NOT NULL,
  title text,
  raw_text text,
  summary text,
  tags text[],
  file_url text,
  is_favorite boolean DEFAULT false,
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now())
);
ALTER TABLE notes DISABLE ROW LEVEL SECURITY;

    Storage: Создайте публичный бакет с именем voice-notes.

🏃 Шаг 5: Запуск

Для полноценной работы нужно запустить два процесса в разных терминалах:

    Запуск бота:

code Bash

python bot.py

    Запуск веб-интерфейса:

code Bash

streamlit run webapp.py

📁 Структура проекта

    bot.py — Интерфейс Telegram и координация сервисов.

    webapp.py — Веб-интерфейс на Streamlit.

    database.py — Слой работы с Supabase (Storage & DB).

    stt_service.py — Обработка аудио и распознавание (Vosk).

    llm_service.py — Анализ и суммаризация (Gemma 2 9b).

    config.py — Загрузка настроек из .env.