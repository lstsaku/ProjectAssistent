from thefuzz import process
from voice_mouse import VoiceMouse
from vision import ScreenVision

class AssistantCore:
    def __init__(self):
        self.mouse = VoiceMouse()
        
        # Расширенная база намерений с учетом доступности
        self.intents = {
            "mouse_up": ["выше", "вверх", "подними"],
            "mouse_down": ["ниже", "вниз", "опусти"],
            "mouse_left": ["левее", "влево"],
            "mouse_right": ["правее", "вправо"],
            "mouse_click_left": ["клик", "нажми", "левый клик", "выбрать"],
            "mouse_click_right": ["правый клик", "свойства", "контекстное меню"],
            "mouse_click_double": ["дважды", "двойной клик", "открой папку"],
            
            # Старые команды для примера
            "open_browser": ["открой браузер", "запусти хром", "интернет"],
            "lock_pc": ["заблокируй комп", "спящий режим"]
        }
        
        self.command_map = {}
        for intent, phrases in self.intents.items():
            for phrase in phrases:
                self.command_map[phrase] = intent

    def process_request(self, user_text):
        if not user_text.strip():
            return "Команда не распознана."

        user_text_lower = user_text.lower()
        
        # Обработка особых модификаторов (например, слова "чуть")
        modifier = "чуть" if "чуть" in user_text_lower or "немного" in user_text_lower else ""

        # Убираем лишние слова для чистоты поиска
        clean_text = user_text_lower.replace("чуть", "").replace("немного", "").strip()

        choices = list(self.command_map.keys())
        best_match, score = process.extractOne(clean_text, choices)

        if score > 70:
            intent = self.command_map[best_match]
            return self.execute_action(intent, modifier)
        else:
            return "Команда не распознана. Попробуйте иначе."

    def execute_action(self, intent, modifier=""):
        # Команды мыши
        if intent == "mouse_up": return self.mouse.move("up", modifier)
        elif intent == "mouse_down": return self.mouse.move("down", modifier)
        elif intent == "mouse_left": return self.mouse.move("left", modifier)
        elif intent == "mouse_right": return self.mouse.move("right", modifier)
        elif intent == "mouse_click_left": return self.mouse.click("left")
        elif intent == "mouse_click_right": return self.mouse.click("right")
        elif intent == "mouse_click_double": return self.mouse.click("double")
        
        # Системные команды
        elif intent == "open_browser":
            # import os; os.system("start chrome") # Раскомментируйте для реального открытия
            return "Открываю браузер..."
            
        return "Действие не найдено."