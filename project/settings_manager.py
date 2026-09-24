import json
import os

class ConfigManager:
    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.config = self.load_config()

    def load_config(self):
        # Если файла нет, создаем базовые настройки
        if not os.path.exists(self.filename):
            default_config = {
                "wake_word": "лиля",
                "mic_index": "Микрофон по умолчанию" # Позже заменим на реальный индекс
            }
            self.save_config(default_config)
            return default_config
        
        # Если файл есть, читаем его
        with open(self.filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_config(self, data=None):
        if data is not None:
            self.config = data
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

    def get(self, key):
        return self.config.get(key)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()