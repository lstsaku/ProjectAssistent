import pytesseract
from PIL import ImageGrab
import re
import os

# Укажите точный путь к установленному Tesseract
# Если при сборке в .exe папка будет лежать рядом, путь нужно будет изменить на os.path.join(os.getcwd(), "Tesseract-OCR", "tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ScreenVision:
    def find_text_coordinates(self, target_text):
        """Ищет слово на экране и возвращает координаты (x, y) его центра"""
        try:
            # Делаем снимок всего экрана в фоне
            screenshot = ImageGrab.grab()
            
            # Получаем данные о тексте (ищем на русском и английском)
            data = pytesseract.image_to_data(screenshot, lang='rus+eng', output_type=pytesseract.Output.DICT)
            
            target_text = target_text.lower().strip()
            
            for i in range(len(data['text'])):
                word = data['text'][i].lower()
                # Очищаем от знаков препинания для точного поиска
                word = re.sub(r'[^\w\s]', '', word)
                
                if target_text in word and len(word) > 1:
                    # Вычисляем центр найденного слова
                    x = data['left'][i]
                    y = data['top'][i]
                    w = data['width'][i]
                    h = data['height'][i]
                    
                    center_x = x + (w // 2)
                    center_y = y + (h // 2)
                    
                    return center_x, center_y
                    
            return None
        except Exception as e:
            print(f"Ошибка зрения. Убедитесь, что Tesseract установлен и путь указан верно: {e}")
            return None