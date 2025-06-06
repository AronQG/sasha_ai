import torch
import soundfile as sf
import numpy as np
import re
import tempfile
import os

# Silero TTS (лучший русский)
model, _ = torch.hub.load(
    repo_or_dir='snakers4/silero-models',
    model='silero_tts',
    language='ru',
    speaker='kseniya_v2'
), None
sample_rate = 16000

def translit_en_to_ru(text):
    # Простейший транслит для tech-названий (можно улучшать таблицей)
    table = str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "абцдефгхийклмнопярстуввксзАбЦДЕФГХИЙКЛМНОПЯРСТУВВКСЗ"
    )
    return text.translate(table)

def split_text_smart(text, max_len=140):
    # Разбиваем по фразам, но не рвем слова
    parts = []
    while len(text) > max_len:
        idx = text.rfind(' ', 0, max_len)
        if idx == -1:
            idx = max_len
        parts.append(text[:idx])
        text = text[idx:].strip()
    if text:
        parts.append(text)
    return parts

def tts_chunk(text):
    # Сначала пытаемся отдать весь текст в Silero (если не получится, транслитерируем)
    try:
        audio = model.apply_tts(text)
        if isinstance(audio, torch.Tensor):
            audio = audio.cpu().numpy()
        elif isinstance(audio, list):
            audio = np.array(audio, dtype=np.float32)
        return audio
    except Exception as ex:
        # Если Silero не понимает - транслитерируем англ слова
        text = re.sub(r'[a-zA-Z0-9]+', lambda m: translit_en_to_ru(m.group()), text)
        audio = model.apply_tts(text)
        if isinstance(audio, torch.Tensor):
            audio = audio.cpu().numpy()
        elif isinstance(audio, list):
            audio = np.array(audio, dtype=np.float32)
        return audio

def text_to_speech(text, output_path="reply.wav"):
    text = str(text).replace('\n', ' ')
    chunks = split_text_smart(text, 120)  # Silero любит покороче
    audios = []
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        audio = tts_chunk(chunk)
        audios.append(audio)
    if not audios:
        raise RuntimeError("Нечего озвучивать (весь текст пустой)")
    audio_full = np.concatenate(audios)
    # Нормализация
    audio_full = audio_full.astype(np.float32)
    audio_full /= max(np.max(np.abs(audio_full)), 1.0)
    sf.write(output_path, audio_full, sample_rate)
    return output_path
