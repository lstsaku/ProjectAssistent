import sounddevice as sd

class AudioManager:
    @staticmethod
    def get_microphones():
        """Сканирует систему и возвращает список доступных микрофонов"""
        mics = []
        try:
            devices = sd.query_devices()
            for i, dev in enumerate(devices):
                if dev['max_input_channels'] > 0:
                    name = dev['name'].strip()
                    mics.append(f"[{i}] {name}")
        except Exception as e:
            print(f"Ошибка при поиске аудиоустройств: {e}")
            
        if not mics:
            return ["Микрофоны не найдены"]
            
        return mics