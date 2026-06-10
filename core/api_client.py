import requests
from datetime import datetime, timedelta


class CBRApiClient:
    BASE_URL = "https://www.cbr-xml-daily.ru"

    @staticmethod
    def get_current_rates():
        """Получает текущие курсы всех валют"""
        try:
            response = requests.get(f"{CBRApiClient.BASE_URL}/daily_json.js")
            response.raise_for_status()
            return response.json()["Valute"]
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении текущих курсов: {e}")
            return {}

    @staticmethod
    def get_current_currency(currency_code: str):
        """Получает текущий курс конкретной валюты"""
        try:
            response = requests.get(f"{CBRApiClient.BASE_URL}/daily_json.js")
            response.raise_for_status()
            data = response.json()["Valute"]
            if currency_code in data:
                return data[currency_code]
            return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении курса {currency_code}: {e}")
            return None

    @staticmethod
    def get_currency_history(currency_code: str, days: int = 30):
        """Получает историю курса конкретной валюты за указанное количество дней"""
        history = []
        today = datetime.now()

        for i in range(days):
            date = today - timedelta(days=i)
            url = f"{CBRApiClient.BASE_URL}/archive/{date.year}/{date.month:02d}/{date.day:02d}/daily_json.js"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()["Valute"]
                    if currency_code in data:
                        history.append({
                            "date": date.strftime("%d.%m.%Y"),
                            "value": data[currency_code]["Value"],
                            "name": data[currency_code]["Name"]
                        })
            except requests.exceptions.RequestException:
                continue

        return list(reversed(history))