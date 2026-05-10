import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import BotCommand

import config
import stt_service
import llm_service
import database


WEBAPP_URL = "http://localhost:8501" # Измените на реальный адрес при деплое

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
user_history = {} # Для контекста LLM

@dp.message(Command("start"))
async def start(m: types.Message):
    await m.answer("🎙 **Smart Voice Notes готовы!**\nОтправьте голосовое сообщение.")

@dp.message(F.voice)
async def handle_voice(message: types.Message):
    if not message.from_user: return
    
    status = await message.answer("📡 Обработка аудио...")
    user_id = message.from_user.id
    file_name = f"{message.voice.file_id}.ogg"
    local_path = os.path.join(config.TEMP_DIR, file_name)

    try:
        # 1. Скачивание
        file = await bot.get_file(message.voice.file_id)
        await bot.download_file(file.file_path, destination=local_path)
        
        # 2. Vosk STT
        await status.edit_text("🔊 Распознаю текст...")
        raw_text = stt_service.transcribe_voice(local_path)
        
        if not raw_text:
            await status.edit_text("❌ Не удалось распознать речь.")
            return

        # 3. Gemma LLM
        await status.edit_text("🧠 Анализирую через Gemma2:9b...")
        context = "\n".join(user_history.get(user_id, [])[-2:])
        analysis = await llm_service.process_text_analysis(raw_text, context)
        
        # 4. Supabase (Бэкенд)
        await status.edit_text("☁️ Сохраняю в облако...")
        file_url = database.upload_to_storage(local_path, file_name)
        database.save_note_to_db(
            user_id=user_id,
            title=analysis['title'],
            raw_text=analysis['text'],
            summary=analysis['summary'],
            tags=analysis['tags'],
            file_url=file_url
        )

        # Сохраняем историю
        user_history.setdefault(user_id, []).append(analysis['summary'])

        await status.edit_text(
            f"✅ **Заметка сохранена!**\n\n"
            f"📌 **{analysis['title']}**\n"
            f"📝 {analysis['summary']}\n\n"
            f"🏷 {', '.join(['#'+t for t in analysis['tags']])}"
        )

        link = f"{WEBAPP_URL}/?u={user_id}"
        
        await status.edit_text(
            f"✅ **Заметка сохранена!**\n\n"
            f"📌 **{analysis['title']}**\n"
            f"📝 {analysis['summary']}\n\n"
            f"🔗 [Открыть в веб-интерфейсе]({link})",
            parse_mode="Markdown"
        )


    except Exception as e:
        await status.edit_text(f"🧨 Ошибка: {str(e)}")
    finally:
        if os.path.exists(local_path): os.remove(local_path)

async def main():
    await bot.set_my_commands([BotCommand(command="start", description="Запуск")])
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())