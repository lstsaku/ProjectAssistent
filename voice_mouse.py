import pyautogui

# Настройки безопасности и плавности
pyautogui.FAILSAFE = False
pyautogui.MINIMUM_DURATION = 0.1

class VoiceMouse:
    def __init__(self):
        self.step = 200        # Обычный шаг в пикселях
        self.small_step = 50   # Мелкий шаг (если сказали "чуть")
    def move_to_absolute(self, x, y):
        """Плавное перемещение в точную координату экрана"""
        pyautogui.moveTo(x, y, duration=0.3) # duration делает движение плавным
        return f"Навел курсор на ({x}, {y})"

    def move(self, direction, modifier=""):
        """Движение курсора в заданном направлении"""
        x, y = pyautogui.position()
        offset = self.small_step if modifier == "чуть" else self.step

        if direction == "up":
            pyautogui.moveTo(x, y - offset)
            return "Двигаю вверх"
        elif direction == "down":
            pyautogui.moveTo(x, y + offset)
            return "Двигаю вниз"
        elif direction == "left":
            pyautogui.moveTo(x - offset, y)
            return "Двигаю влево"
        elif direction == "right":
            pyautogui.moveTo(x + offset, y)
            return "Двигаю вправо"
            
    def click(self, button="left"):
        """Клик мышью"""
        if button == "left":
            pyautogui.click()
            return "Левый клик"
        elif button == "right":
            pyautogui.rightClick()
            return "Правый клик"
        elif button == "double":
            pyautogui.doubleClick()
            return "Двойной клик"

    def type_text(self, text):
        """Печать текста с клавиатуры"""
        pyautogui.write(text, interval=0.05)
        return f"Напечатано: {text}"