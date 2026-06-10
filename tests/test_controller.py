import unittest
from unittest.mock import MagicMock, patch
from modules.currency_tracker.controller import CurrencyTrackerController


class TestCurrencyTrackerController(unittest.TestCase):

    def setUp(self):
        """Настраивается перед каждым тестом"""
        # Создаем мок для view
        self.mock_view = MagicMock()
        self.controller = CurrencyTrackerController(self.mock_view)

    @patch('core.api_client.CBRApiClient.get_current_currency')
    @patch('core.api_client.CBRApiClient.get_currency_history')
    def test_load_data_success(self, mock_history, mock_current):
        """Тест успешной загрузки данных"""
        # Мокаем данные от API
        mock_current.return_value = {"Value": 92.5, "Name": "Доллар США"}
        mock_history.return_value = [
            {"date": "01.01.2024", "value": 90.0, "name": "Доллар США"},
            {"date": "02.01.2024", "value": 91.5, "name": "Доллар США"},
            {"date": "03.01.2024", "value": 92.5, "name": "Доллар США"}
        ]

        # Вызываем метод
        self.controller.load_data("USD", 3)

        # Проверяем, что view был обновлен
        self.mock_view.set_loading_state.assert_called()
        self.mock_view.update_chart.assert_called_once()
        self.mock_view.update_stats.assert_called_once()

        # Проверяем параметры вызова update_stats
        call_args = self.mock_view.update_stats.call_args
        self.assertEqual(call_args[1]['current_value'], 92.5)
        self.assertEqual(call_args[1]['min_value'], 90.0)
        self.assertEqual(call_args[1]['max_value'], 92.5)

    @patch('core.api_client.CBRApiClient.get_current_currency')
    @patch('core.api_client.CBRApiClient.get_currency_history')
    def test_load_data_empty_history(self, mock_history, mock_current):
        """Тест обработки пустой истории"""
        mock_current.return_value = {"Value": 92.5, "Name": "Доллар США"}
        mock_history.return_value = []

        self.controller.load_data("USD", 3)

        # Должна быть показана ошибка
        self.mock_view.show_error.assert_called_once()

    @patch('core.api_client.CBRApiClient.get_current_currency')
    def test_convert_currency_success(self, mock_current):
        """Тест успешной конвертации валюты"""
        mock_current.return_value = {"Value": 92.5, "Name": "Доллар США"}

        self.controller.convert_currency(100.0, "USD")

        # Проверяем, что результат обновлен
        self.mock_view.update_conversion_result.assert_called_once_with(9250.0, 92.5)

    @patch('core.api_client.CBRApiClient.get_current_currency')
    def test_convert_currency_error(self, mock_current):
        """Тест обработки ошибки при конвертации"""
        mock_current.return_value = None

        self.controller.convert_currency(100.0, "USD")

        # Должна быть показана ошибка
        self.mock_view.show_error.assert_called_once()


if __name__ == '__main__':
    unittest.main()