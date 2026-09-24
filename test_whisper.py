import os
# Перенаправляем папку кэша моделей на диск F в папку вашего проекта
os.environ["TORCH_HOME"] = r"F:\Проги\project\cache"
os.environ["WHISPER_CACHEDIR"] = r"F:\Проги\project\cache"

from whisper_listener import WhisperListener


if __name__ == "__main__":
    # Инициализируем слушатель (при первом запуске модель 'tiny' скачает около 39 МБ)
    listener = WhisperListener(model_size="tiny")
    
    print("\n--- Тест запущен! ---")
    print("Через 2 секунды скажите что-нибудь в микрофон (например: 'Привет, Лиля, открой браузер').")
    
    import time
    time.sleep(2)
    
    # Записываем 5 секунд аудио
    text = listener.listen_and_transcribe(duration=5)
    
    print("\nРезультат теста:")
    if text:
        print(f"Вы сказали: {text}")
    else:
        print("Ничего не удалось распознать. Проверьте микрофон.")