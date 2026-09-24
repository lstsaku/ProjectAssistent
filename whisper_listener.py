import os
import whisper
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile as wavfile

class WhisperListener:
    def __init__(self, model_size="tiny"):
        print(f"Загружаю модель Whisper ({model_size})... При первом запуске она скачается автоматически.")
        # Загружаем локальную модель (tiny работает быстрее всего на CPU)
        self.model = whisper.load_model(model_size)
        print("Whisper успешно загружена и готова к работе!")

    def listen_and_transcribe(self, duration=4, samplerate=16000):
        """Записывает звук с микрофона и возвращает распознанный текст"""
        print("Слушаю...")
        
        # Запись аудио с микрофона
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.float32)
        sd.wait()
        
        audio_data = np.squeeze(audio_data)
        audio_int16 = (audio_data * 32767).astype(np.int16)

        # Сохранение во временный файл для Whisper
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            temp_filename = f.name
        
        wavfile.write(temp_filename, samplerate, audio_int16)

        try:
            # Распознавание речи через Whisper
            result = self.model.transcribe(temp_filename, language="ru")
            text = result.get("text", "").strip()
            print(f"Распознано: '{text}'")
            return text
        except Exception as e:
            print(f"Ошибка распознавания: {e}")
            return ""
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)