import os
from thefuzz import process

class AppFinder:
    def __init__(self):
        self.installed_apps = {}
        self.scan_pc()

    def scan_pc(self):
        """Сканирует все ярлыки на ПК"""
        paths_to_scan = [
            os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"),
            r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
            r"C:\Program Files",
            r"C:\Program Files (x86)"
        ]

        for base_path in paths_to_scan:
            if os.path.exists(base_path):
                for root, dirs, files in os.walk(base_path):
                    for file in files:
                        if file.endswith(".lnk") or file.endswith(".exe"):
                            app_name = os.path.splitext(file)[0].lower()
                            full_path = os.path.join(root, file)
                            self.installed_apps[app_name] = full_path

    def find_and_launch(self, query):
        """Умный поиск с обработкой корней и сокращений без огромных списков"""
        query = query.lower().strip()
        if not query:
            return "Укажите название приложения."

        if not self.installed_apps:
            return "Список приложений пуст."

        choices = list(self.installed_apps.keys())
        
        # 1. Пробуем найти точное или нечеткое совпадение по первому слову/корню
        # Например, если сказали "телега", ищем приложения, которые начинаются с "тел"
        best_match, score = process.extractOne(query, choices)
        
        # Если совпадение хорошее (>50%) ИЛИ пользователь назвал корень слова (например, первые 4 буквы)
        if score > 50 or any(query in choice for choice in choices):
            # Если точного попадания по баллам нет, но корень содержится в имени программы
            if score <= 50:
                best_match = next((choice for choice in choices if query in choice), choices[0])

            app_path = self.installed_apps[best_match]
            try:
                os.startfile(app_path)
                return f"Запускаю: {best_match}"
            except Exception as e:
                return f"Ошибка запуска: {e}"
        else:
            # Запасной вариант через системный вызов Windows
            try:
                os.system(f"start {query}")
                return f"Пытаюсь запустить: {query}"
            except Exception:
                return f"Не удалось найти приложение '{query}'."