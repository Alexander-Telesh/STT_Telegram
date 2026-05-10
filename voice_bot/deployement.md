# Smart Voice Notes: Deployment Guide

Сервис для создания структурированных заметок из голосовых сообщений Telegram.

Стек проекта:
- Telegram Bot (`aiogram`)
- Speech-to-Text (`vosk`, `pydub`, `ffmpeg`)
- LLM-анализ (`ollama`, модель `gemma2:9b`)
- Хранение (`supabase`: DB + Storage)
- Веб-интерфейс (`streamlit`)

## 1) Системные требования

- ОС: Linux / macOS / Windows
- RAM: от 16 GB (для локальной работы `gemma2:9b`)
- Установленный `ffmpeg`
- Python 3.10+
- Установленный и запущенный `ollama`

## 2) Установка зависимостей

### Linux (Ubuntu)

```bash
sudo apt update
sudo apt install -y ffmpeg python3-venv wget unzip
```

### macOS

```bash
brew install ffmpeg
```

### Python-окружение

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 3) Настройка конфигурации

Сейчас проект читает настройки напрямую из `config.py`.
Перед запуском обязательно проверьте и укажите корректные значения:

- `BOT_TOKEN`
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `VOSK_MODEL_PATH` (по умолчанию `model`)
- `LLM_MODEL` (по умолчанию `gemma2:9b`)

## 4) Установка моделей

### Vosk (русская модель)

```bash
wget https://alphacephei.com/vosk/models/vosk-model-ru-0.42.zip
unzip vosk-model-ru-0.42.zip
mv vosk-model-ru-0.42 model
rm vosk-model-ru-0.42.zip
```

### Ollama (LLM)

```bash
ollama pull gemma2:9b
```

Убедитесь, что сервис Ollama запущен и доступен локально.

## 5) Настройка Supabase

### 5.1 Таблица `notes`

Выполните SQL в Supabase SQL Editor:

```sql
create table if not exists notes (
  id uuid default gen_random_uuid() primary key,
  user_id bigint not null,
  title text,
  raw_text text,
  summary text,
  tags text[],
  file_url text,
  is_favorite boolean default false,
  created_at timestamp with time zone default timezone('utc'::text, now())
);
```

### 5.2 Storage bucket

Создайте публичный bucket с именем `voice-notes`.

## 6) Запуск приложения

Нужно запустить два процесса в разных терминалах.

### 6.1 Telegram-бот

```bash
source venv/bin/activate
python bot.py
```

### 6.2 Web UI (Streamlit)

```bash
source venv/bin/activate
streamlit run webapp.py
```

После сохранения заметки бот отправит ссылку вида:

`http://localhost:8501/?u=<telegram_user_id>`

## 7) Быстрая диагностика

- Если не распознается речь: проверьте `ffmpeg` и наличие модели в `model/`.
- Если не работает анализ: проверьте `ollama` и наличие модели `gemma2:9b`.
- Если нет сохранения заметок: проверьте `SUPABASE_URL`, `SUPABASE_KEY`, таблицу `notes` и bucket `voice-notes`.