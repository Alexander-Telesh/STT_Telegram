# llm_service.py
import ollama
import asyncio
from config import LLM_MODEL

async def process_text_analysis(raw_text: str, context: str = "") -> dict:
    """Gemma исправляет ослышки Vosk на основе смысла фразы"""
    
    prompt = f"""
    Ты — эксперт по исправлению ошибок распознавания речи. 
    Текст ниже содержит "ослышки" (слова, замененные на похожие по звуку).
    
    ТВОИ ПРАВИЛА:
    1. ИСПРАВЛЯЙ ПО СМЫСЛУ: Если написано "я мне хочу", исправь на "я не хочу". 
    2. ВОССТАНАВЛИВАЙ СВЯЗИ: Vosk часто путает предлоги и окончания. Сделай текст грамматически верным.
    3. НЕ МЕНЯЙ СЛОВА: Если слово понятно и логично, не заменяй его синонимом. Оставь авторский стиль.
    4. УДАЛЯЙ МУСОР: Повторяющиеся слоги или бессмысленные звуки ("ыы", "мм", "пр") удаляй.

    ВЫВЕДИ В ФОРМАТЕ:
    Title: [Краткий заголовок]
    Text: [Исправленный полный текст]
    Summary: [Суть в 1-2 предложениях]
    Tags: [тег1, тег2]

    КОНТЕКСТ ПРОШЛОГО: {context}
    СЫРОЙ ТЕКСТ: "{raw_text}"
    """
    
    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(
        None, 
        lambda: ollama.generate(
            model=LLM_MODEL, 
            prompt=prompt, 
            options={"temperature": 0.1, "top_p": 0.9} # Низкая температура для точности
        )
    )
    res_text = response['response']
    
    # Парсинг (оставляем старый)
    result = {"title": "Новая заметка", "text": raw_text, "summary": "", "tags": []}
    for line in res_text.split('\n'):
        line = line.strip()
        if line.startswith("Title:"): result["title"] = line.replace("Title:", "").strip()
        if line.startswith("Text:"): result["text"] = line.replace("Text:", "").strip()
        if line.startswith("Summary:"): result["summary"] = line.replace("Summary:", "").strip()
        if line.startswith("Tags:"): 
            tags_raw = line.replace("Tags:", "").strip()
            result["tags"] = [t.strip().lower() for t in tags_raw.split(',')]
            
    return result