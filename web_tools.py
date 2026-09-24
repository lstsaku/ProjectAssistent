import requests
import webbrowser

class WebTools:
    def get_location(self):
        """Автоматически определяет город пользователя по IP"""
        try:
            # Бесплатный сервис геолокации по IP
            response = requests.get("https://ipapi.co/json/", timeout=3)
            if response.status_code == 200:
                data = response.json()
                city = data.get("city", "Москва")
                return city
        except Exception as e:
            print(f"Не удалось определить город: {e}")
        return "Москва" # Город по умолчанию на случай сбоя интернета

    def get_weather(self, city=None):
        """Получает погоду для указанного или текущего города"""
        if not city:
            city = self.get_location()
        try:
            # Сервис wttr.in выдает готовую текстовую погоду
            url = f"https://wttr.in/{city}?format=3&lang=ru"
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                return f"Погода в городе {city}: {response.text.strip()}"
        except Exception as e:
            print(f"Ошибка получения погоды: {e}")
        return "Не удалось получить данные о погоде."

    def get_currency(self):
        """Получает текущий курс доллара и евро от Центробанка РФ"""
        try:
            url = "https://www.cbr-xml-daily.ru/daily_json.js"
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                data = response.json()
                usd = data['Valute']['USD']['Value']
                eur = data['Valute']['EUR']['Value']
                return f"Курс валют ЦБ: Доллар — {usd:.2f} руб., Евро — {eur:.2f} руб."
        except Exception as e:
            print(f"Ошибка получения курсов валют: {e}")
        return "Не удалось загрузить курсы валют."

    def search_in_browser(self, query):
        """Открывает браузер с поисковым запросом"""
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"Ищу в интернете: {query}"