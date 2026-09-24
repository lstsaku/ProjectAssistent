from thefuzz import process
from voice_mouse import VoiceMouse
from vision import ScreenVision
from web_tools import WebTools 
from app_finder import AppFinder

class AssistantCore:
    def __init__(self):
        self.mouse = VoiceMouse()
        self.vision = ScreenVision()
        self.web = WebTools() 
        self.app_finder = AppFinder()
        self.intents = {
            "mouse_up": ["выше", "вверх", "подними"],
            "mouse_down": ["ниже", "вниз", "опусти"],
            "mouse_left": ["левее", "влево"],
            "mouse_right": ["правее", "вправо"],
            "mouse_click_left": ["клик", "нажми", "левый клик", "выбрать"],
            "mouse_click_right": ["правый клик", "свойства"],
            
            # Новые веб-интенты
            "weather": ["погода", "какая погода", "температура"],
            "currency": ["курс", "доллар", "евро", "курс валют"],
            
            "open_browser": ["открой браузер", "запусти хром", "интернет"],
            "mute_volume": ["выключи звук", "тишина"],
            "lock_pc": ["заблокируй комп", "спящий режим"]
        }
        
        self.command_map = {}
        for intent, phrases in self.intents.items():
            for phrase in phrases:
                self.command_map[phrase] = intent

    def process_request(self, user_text):
        if not user_text.strip():
            return "Команда не распознана."

        user_text_lower = user_text.lower().strip()

        # Зрение (OCR)
        if user_text_lower.startswith("наведи на ") or user_text_lower.startswith("найди "):
            target = user_text_lower.replace("наведи на ", "").replace("найди ", "").strip()
            coords = self.vision.find_text_coordinates(target)
            if coords:
                self.mouse.move_to_absolute(coords[0], coords[1])
                return f"Элемент '{target}' найден."
            return f"Я не вижу '{target}' на экране."

        # Прямой поиск в интернете, если сказали "найди в интернете" или "загугли"
        if user_text_lower.startswith("найди в интернете ") or user_text_lower.startswith("загугли "):
            query = user_text_lower.replace("найди в интернете ", "").replace("загугли ", "").strip()
            return self.web.search_in_browser(query)

        # Запуск установленных программ на ПК
        if user_text_lower.startswith("открой ") or user_text_lower.startswith("запусти "):
         app_query = user_text_lower.replace("открой ", "").replace("запусти ", "").strip()
         return self.app_finder.find_and_launch(app_query)
        
        # Нечеткий поиск по фиксированным командам
        modifier = "чуть" if "чуть" in user_text_lower or "немного" in user_text_lower else ""
        clean_text = user_text_lower.replace("чуть", "").replace("немного", "").strip()

        choices = list(self.command_map.keys())
        best_match, score = process.extractOne(clean_text, choices)

        if score > 70:
            intent = self.command_map[best_match]
            return self.execute_action(intent, modifier)
        else:
            return "Команда не распознана. Попробуйте иначе."

    def execute_action(self, intent, modifier=""):
        if intent == "mouse_up": return self.mouse.move("up", modifier)
        elif intent == "mouse_down": return self.mouse.move("down", modifier)
        elif intent == "mouse_left": return self.mouse.move("left", modifier)
        elif intent == "mouse_right": return self.mouse.move("right", modifier)
        elif intent == "mouse_click_left": return self.mouse.click("left")
        elif intent == "mouse_click_right": return self.mouse.click("right")
        
        # Обработка веб-функций
        elif intent == "weather":
            city = self.web.get_location()
            return self.web.get_weather(city)
        elif intent == "currency":
            return self.web.get_currency()
            
        elif intent == "open_browser":
            return self.web.search_in_browser("google.com")
        elif intent == "mute_volume":
            return "Звук отключен."
        elif intent == "lock_pc":
            return "Блокирую систему..."
            
        return "Действие не найдено."