import sounddevice as sd
import numpy as np
import queue
import tempfile
import soundfile as sf
from interfaces.tts import text_to_speech
from interfaces.stt import speech_to_text

def record_audio(duration=6, fs=16000):
    print("Говори... (запись %d сек)" % duration)
    q = queue.Queue()
    def callback(indata, frames, time, status):
        q.put(indata.copy())
    with sd.InputStream(samplerate=fs, channels=1, dtype='float32', callback=callback):
        frames = []
        for _ in range(int(fs / 1024 * duration)):
            frames.append(q.get())
        audio = np.concatenate(frames, axis=0)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(tmp.name, audio, fs)
    return tmp.name

def local_voice_loop(agent):
    import simpleaudio as sa
    user = "local_user"
    print("Саша готова! Нажми Enter, чтобы поговорить, или 'q' для выхода.")
    while True:
        inp = input(">> Нажми Enter для записи (или 'q' + Enter для выхода):\n")
        if inp.strip().lower() == "q":
            break
        audio_path = record_audio()
        text = speech_to_text(audio_path)
        print("Ты сказал:", text)
        answer = agent.handle_message(user, text)
        print("Саша:", answer)
        voice_path = text_to_speech(answer)
        wave_obj = sa.WaveObject.from_wave_file(voice_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()
