from core.api_client import CBRApiClient


class CurrencyTrackerController:
    def __init__(self, view):
        self.view = view
        self.api_client = CBRApiClient()

        self.view.update_requested.connect(self.load_data)
        self.view.convert_requested.connect(self.convert_currency)

    def load_data(self, currency_code: str, days: int):
        self.view.set_loading_state(True)

        # Получаем текущий курс
        current_data = self.api_client.get_current_currency(currency_code)

        # Получаем историю
        history = self.api_client.get_currency_history(currency_code, days)

        if history:
            dates = [item["date"] for item in history]
            values = [item["value"] for item in history]
            name = history[0]["name"]

            # Вычисляем статистику
            min_value = min(values)
            max_value = max(values)
            current_value = values[-1] if values else 0
            previous_value = values[-2] if len(values) > 1 else current_value

            # Изменение за день в процентах
            if previous_value > 0:
                change_percent = ((current_value - previous_value) / previous_value) * 100
            else:
                change_percent = 0

            self.view.update_chart(dates, values, name, change_percent >= 0)
            self.view.update_stats(
                current_value=current_value,
                change_percent=change_percent,
                min_value=min_value,
                max_value=max_value,
                currency_name=name
            )
        else:
            self.view.show_error("Не удалось загрузить данные. Проверьте интернет-соединение.")

        self.view.set_loading_state(False)

    def convert_currency(self, amount: float, currency_code: str):
        """Конвертирует валюту"""
        current_data = self.api_client.get_current_currency(currency_code)
        if current_data:
            rate = current_data["Value"]
            result = amount * rate
            self.view.update_conversion_result(result, rate)
        else:
            self.view.show_error("Не удалось получить текущий курс для конвертации.")