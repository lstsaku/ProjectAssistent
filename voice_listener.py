import sounddevice as sd
import vosk
import json
import queue
import threading
import sys

vosk.SetLogLevel(-1) 

class VoiceListener:
    def __init__(self, config_manager, on_command_callback):
        self.config = config_manager
        self.callback = on_command_callback
        self.q = queue.Queue()
        self.running = False
        
        try:
            # Берем модель напрямую с диска F (без кириллицы в пути)
            model_path = r"F:\model"
            print(f"Загружаю модель Vosk из: {model_path}")
            
            self.model = vosk.Model(model_path)
            print("Vosk: Языковая модель успешно загружена.")
        except Exception as e:
            print(f"Ошибка загрузки модели Vosk: {e}")
            self.model = None

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def listen_loop(self):
        if not self.model:
            return

        wake_word = self.config.get("wake_word").lower().strip()
        mic_string = self.config.get("mic_index")
        
        mic_index = None
        if mic_string and isinstance(mic_string, str) and "[" in mic_string:
            try:
                mic_index = int(mic_string.split("[")[1].split("]")[0])
            except ValueError:
                pass

        try:
            samplerate = 16000
            with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=mic_index, 
                                   dtype='int16', channels=1, callback=self.audio_callback):
                
                print(f"Слушаю микрофон... Жду обращение: '{wake_word}'")
                rec = vosk.KaldiRecognizer(self.model, samplerate)
                
                while self.running:
                    data = self.q.get()
                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        text = result.get("text", "").lower()
                        
                        if text:
                            # Проверяем, есть ли имя (wake word) во фразе
                            if wake_word in text:
                                command = text.split(wake_word, 1)[-1].strip()
                                self.callback(command)
        except Exception as e:
            print(f"Ошибка аудиопотока: {e}")

    def start(self):
        if self.running: return
        self.running = True
        self.thread = threading.Thread(target=self.listen_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False