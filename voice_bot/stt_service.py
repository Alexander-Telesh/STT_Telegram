# stt_service.py
import json
import io
import os
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer
from config import VOSK_MODEL_PATH

# Загружаем модель
vosk_model = Model(VOSK_MODEL_PATH)

def transcribe_voice(file_path: str) -> str:
    """Улучшенная обработка звука для минимизации ошибок"""
    audio = AudioSegment.from_file(file_path)
    
    # 1. Принудительное приведение к моно и 16кГц
    audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    
    # 2. ДИНАМИЧЕСКОЕ СЖАТИЕ (Компрессия)
    # Это делает тихие звуки (окончания слов) громче, а громкие — тише.
    # Vosk намного лучше распознает сжатый диапазон.
    audio = audio.normalize().compress_dynamic_range()
    
    # 3. ФИЛЬТРАЦИЯ ЧАСТОТ
    # Голос человека обычно в диапазоне 200Гц - 5000Гц. Остальное — шум.
    audio = audio.high_pass_filter(200).low_pass_filter(5000)

    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)

    rec = KaldiRecognizer(vosk_model, 16000)
    # Включаем вывод слов с их "уверенностью" (опционально для больших моделей)
    rec.SetWords(True) 

    full_text = []
    while True:
        data = wav_io.read(16000)
        if len(data) == 0: break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            if res.get("text"):
                full_text.append(res["text"])
    
    res = json.loads(rec.FinalResult())
    if res.get("text"):
        full_text.append(res["text"])
    
    return " ".join(full_text)