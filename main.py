import customtkinter as ctk
from core import AssistantCore
from settings_manager import ConfigManager
from voice_listener import VoiceListener
from audio_manager import AudioManager

# Настройка внешнего вида
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, master, config_manager):
        super().__init__(master)
        
        self.config_manager = config_manager
        
        self.title("Настройки ассистента")
        self.geometry("350x250")
        self.resizable(False, False)
        
        # Перехватываем фокус на это окно
        self.grab_set()

        # --- Заголовок ---
        self.label = ctk.CTkLabel(self, text="Параметры", font=("Roboto", 18, "bold"))
        self.label.pack(pady=(15, 10))

        # --- Настройка Имени (Wake word) ---
        self.name_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.name_frame.pack(fill="x", padx=20, pady=5)
        
        self.name_label = ctk.CTkLabel(self.name_frame, text="Имя ассистента:")
        self.name_label.pack(side="left")
        
        self.name_entry = ctk.CTkEntry(self.name_frame, width=150)
        self.name_entry.pack(side="right")
        # Подгружаем текущее имя из конфига
        current_name = self.config_manager.get("wake_word")
        self.name_entry.insert(0, current_name)

       # --- Выбор микрофона ---
        self.mic_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.mic_frame.pack(fill="x", padx=20, pady=10)
        
        self.mic_label = ctk.CTkLabel(self.mic_frame, text="Микрофон:")
        self.mic_label.pack(side="left")
        
        # Получаем реальный список микрофонов из системы
        real_microphones = AudioManager.get_microphones()
        
        self.mic_option = ctk.CTkOptionMenu(self.mic_frame, values=real_microphones, width=200)
        self.mic_option.pack(side="right")
        
        saved_mic = self.config_manager.get("mic_index")
        if saved_mic in real_microphones:
            self.mic_option.set(saved_mic)
        else:
            self.mic_option.set(real_microphones[0])
            
        # --- Кнопка Сохранить ---
        self.save_btn = ctk.CTkButton(self, text="Сохранить", command=self.save_settings)
        self.save_btn.pack(side="bottom", pady=20)

    def save_settings(self):
        # Получаем данные из полей
        new_name = self.name_entry.get().lower().strip()
        new_mic = self.mic_option.get()
        
        # Сохраняем в JSON
        self.config_manager.set("wake_word", new_name)
        self.config_manager.set("mic_index", new_mic)
        
        # Закрываем окно
        self.destroy()

class AssistantApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.core = AssistantCore()
        self.config = ConfigManager() # Инициализируем настройки

        self.title("Nexus Assistant")
        self.geometry("400x500")
        self.resizable(False, False)

        # Верхняя панель (Заголовок + Кнопка настроек)
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(fill="x", padx=20, pady=(15, 0))

        self.label_title = ctk.CTkLabel(self.top_frame, text="Nexus Assist", font=("Roboto", 20, "bold"))
        self.label_title.pack(side="left")

        self.btn_settings = ctk.CTkButton(self.top_frame, text="⚙ Настройки", width=30, command=self.open_settings)
        self.btn_settings.pack(side="right")

        # Поле вывода ответов
        self.textbox = ctk.CTkTextbox(self, width=350, height=330, corner_radius=10)
        self.textbox.pack(pady=10)
        self.textbox.configure(state="disabled")

        # Поле ввода текста
        self.entry_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.entry_frame.pack(pady=10, fill="x", padx=20)

        self.user_input = ctk.CTkEntry(self.entry_frame, placeholder_text="Введите команду...", width=250)
        self.user_input.pack(side="left", padx=(0, 10))
        self.user_input.bind("<Return>", self.send_command)

        self.btn_send = ctk.CTkButton(self.entry_frame, text="Отправить", width=90, command=self.send_command)
        self.btn_send.pack(side="left")
        
        # Приветствие с учетом имени
        current_name = self.config.get("wake_word").capitalize()
        self.log_message(f"Система запущена. Мое имя: {current_name}.", sender="Система")
# Запускаем голосовое прослушивание
        self.listener = VoiceListener(self.config, self.on_voice_command)
        self.listener.start()

    def on_voice_command(self, text):
        """Перехватывает голос и отправляет в чат и ядро"""
        if not text:
            self.log_message("Слушаю...", sender="Голос")
            return

        self.log_message(text, sender="Вы (Голос)")
        response = self.core.process_request(text)
        self.log_message(response)
    def open_settings(self):
        # Открываем окно настроек, передаем в него наш config_manager
        SettingsWindow(self, self.config)

    def log_message(self, text, sender="Ассистент"):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", f"{sender}: {text}\n\n")
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def send_command(self, event=None):
        text = self.user_input.get()
        if not text:
            return

        self.log_message(text, sender="Вы")
        self.user_input.delete(0, "end")
        
        response = self.core.process_request(text)
        self.log_message(response)

if __name__ == "__main__":
    app = AssistantApp()
    app.mainloop()