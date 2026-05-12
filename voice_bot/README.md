# Данные об авторе

Фамилия имя отчество: Телеш Александр Сергеевич

Логин: telesh_as_23 

Курс / семестр: 3 курс / 6 семестр

Специальность: 1-40 03 01 «Искусственный интеллект»

Вид проекта: Курсовая работа

# Название проекта

Создание заметок из голосовых сообщений

#Краткое описание:
Программа представляет собой интеллектуальную систему, состоящую из Telegram-бота и веб-интерфейса. Бот принимает голосовые сообщения, конвертирует их в текст с помощью локальной модели Vosk Large 0.42, после чего текст обрабатывается большой языковой моделью Gemma2 (через Ollama) для исправления грамматических ошибок, создания краткого резюме (summary) и расстановки тегов. Данные синхронизируются с облачной базой данных и хранилищем Supabase, а пользователь может управлять своим архивом заметок через интерактивный дашборд на Streamlit.


    
# Smart Voice Notes

Smart Voice Notes - проект для обработки голосовых сообщений из Telegram с автоматической расшифровкой, исправлением текста и сохранением заметок в Supabase.

## Возможности

- Прием голосовых сообщений в Telegram-боте
- Распознавание речи через `vosk`
- Очистка и структурирование текста через `ollama` (`gemma2:9b`)
- Сохранение заметок и аудио в Supabase (DB + Storage)
- Просмотр заметок в веб-интерфейсе на Streamlit

## Для корректной работы проекта необходимы следующие компоненты:

Язык программирования: Python 3.10+

Системные зависимости:

FFmpeg — для декодирования и обработки аудиофайлов.

Ollama — для запуска локальной LLM-модели (требуется установленная модель gemma2:9b).

Библиотеки Python (основные):

aiogram 3.x — для реализации Telegram-бота.

vosk — для оффлайн распознавания речи.

pydub — для манипуляций с аудио (нормализация, фильтрация).

supabase — для взаимодействия с базой данных и облачным хранилищем.

streamlit — для визуализации веб-интерфейса.

ollama — для интеграции с нейросетью-корректором.

Аппаратные требования:

Минимум 16 ГБ оперативной памяти (для одновременной работы Vosk Large и Gemma2).

Наличие свободного места на диске (~2 ГБ для весов Vosk и ~5.5 ГБ для Gemma2).

## Структура проекта

- `bot.py` - Telegram-бот и основной сценарий обработки
- `stt_service.py` - обработка аудио и STT
- `llm_service.py` - промпт и парсинг ответа LLM
- `database.py` - слой доступа к Supabase
- `webapp.py` - Streamlit интерфейс заметок
- `config.py` - конфигурация проекта
- `deployement.md` - подробный гайд по деплою

## Быстрый старт

### 1. Установите системные зависимости

Для Linux (Ubuntu):

```bash
sudo apt update
sudo apt install -y ffmpeg python3-venv wget unzip
```

Для macOS:

```bash
brew install ffmpeg
```

### 2. Создайте Python-окружение и установите зависимости

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Настройте `config.py`

Заполните рабочие значения в `config.py`:

- `BOT_TOKEN`
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `VOSK_MODEL_PATH` (обычно `model`)
- `LLM_MODEL` (обычно `gemma2:9b`)

### 4. Установите модель Vosk

```bash
wget https://alphacephei.com/vosk/models/vosk-model-ru-0.42.zip
unzip vosk-model-ru-0.42.zip
mv vosk-model-ru-0.42 model
rm vosk-model-ru-0.42.zip
```

### 5. Установите и подготовьте Ollama

```bash
ollama pull gemma2:9b
```

Убедитесь, что Ollama запущен.

### 6. Подготовьте Supabase

Создайте таблицу:

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

И создайте публичный bucket `voice-notes`.

## Запуск

Откройте два терминала.

Терминал 1 (бот):

```bash
source venv/bin/activate
python bot.py
```

Терминал 2 (веб):

```bash
source venv/bin/activate
streamlit run webapp.py
```

## Как работает поток данных

1. Пользователь отправляет голосовое сообщение в Telegram.
2. Бот скачивает `.ogg` во временную папку.
3. `stt_service.py` конвертирует звук и распознает текст через Vosk.
4. `llm_service.py` корректирует текст и создает summary/tags.
5. `database.py` загружает аудио в Supabase Storage и сохраняет заметку в таблицу `notes`.
6. Пользователь открывает заметку в Streamlit по ссылке из бота.

## Диагностика

- Ошибка распознавания: проверьте модель в `model/` и наличие `ffmpeg`.
- Ошибка анализа LLM: проверьте `ollama` и модель `gemma2:9b`.
- Ошибка Supabase: проверьте токен/URL, таблицу `notes` и bucket `voice-notes`.

## Примечание по безопасности

Секреты сейчас хранятся в `config.py`. Для продакшена рекомендуется перенести их в переменные окружения и исключить из git.
