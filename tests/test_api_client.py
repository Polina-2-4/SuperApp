import unittest
from unittest.mock import patch, MagicMock
from core.api_client import CBRApiClient


class TestCBRApiClient(unittest.TestCase):

    def setUp(self):
        """Настраивается перед каждым тестом"""
        self.client = CBRApiClient()

    @patch('core.api_client.requests.get')
    def test_get_current_rates_success(self, mock_get):
        """Тест успешного получения текущих курсов"""
        # Мокаем ответ API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 92.5, "Name": "Доллар США"},
                "EUR": {"Value": 100.2, "Name": "Евро"}
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Вызываем метод
        result = self.client.get_current_rates()

        # Проверяем результат
        self.assertIn("USD", result)
        self.assertIn("EUR", result)
        self.assertEqual(result["USD"]["Value"], 92.5)
        mock_get.assert_called_once()

    @patch('core.api_client.requests.get')
    def test_get_current_rates_error(self, mock_get):
        """Тест обработки ошибки при получении курсов"""
        import requests
        mock_get.side_effect = requests.exceptions.RequestException("Ошибка сети")

        result = self.client.get_current_rates()

        # При ошибке должен вернуться пустой словарь
        self.assertEqual(result, {})

    @patch('core.api_client.requests.get')
    def test_get_current_currency(self, mock_get):
        """Тест получения курса конкретной валюты"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 92.5, "Name": "Доллар США"},
                "EUR": {"Value": 100.2, "Name": "Евро"}
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = self.client.get_current_currency("USD")

        self.assertIsNotNone(result)
        self.assertEqual(result["Value"], 92.5)
        self.assertEqual(result["Name"], "Доллар США")

    @patch('core.api_client.requests.get')
    def test_get_current_currency_not_found(self, mock_get):
        """Тест получения несуществующей валюты"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 92.5, "Name": "Доллар США"}
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = self.client.get_current_currency("XYZ")

        self.assertIsNone(result)

    @patch('core.api_client.requests.get')
    def test_get_currency_history(self, mock_get):
        """Тест получения истории курсов"""
        # Мокаем ответ для нескольких дней
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 92.5, "Name": "Доллар США"}
            }
        }
        mock_get.return_value = mock_response

        # Запрашиваем историю за 3 дня
        history = self.client.get_currency_history("USD", days=3)

        # Должны получить 3 записи (или меньше, если какие-то дни пропущены)
        self.assertLessEqual(len(history), 3)
        if history:
            self.assertIn("date", history[0])
            self.assertIn("value", history[0])
            self.assertIn("name", history[0])


if __name__ == '__main__':
    unittest.main()