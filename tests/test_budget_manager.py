import unittest
import os
from unittest.mock import MagicMock
from modules.budget_manager.models import BudgetModel
from modules.budget_manager.controller import BudgetController


class TestBudgetModel(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_budget_data.json"
        self.model = BudgetModel(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_income_transaction(self):
        """Тест добавления дохода"""
        self.model.add_transaction("income", 15000.0, "Стипендия", "Ежемесячная")

        transactions = self.model.data['transactions']
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['type'], 'income')
        self.assertEqual(transactions[0]['amount'], 15000.0)

    def test_add_expense_transaction(self):
        """Тест добавления расхода"""
        self.model.add_transaction("expense", 500.0, "Еда", "Продукты")

        transactions = self.model.data['transactions']
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['type'], 'expense')
        self.assertEqual(transactions[0]['amount'], 500.0)

    def test_calculate_balance_positive(self):
        """Тест расчета положительного баланса"""
        self.model.add_transaction("income", 15000.0, "Стипендия", "")
        self.model.add_transaction("expense", 3000.0, "Еда", "")

        balance = self.model.get_balance()
        self.assertEqual(balance, 12000.0)

    def test_calculate_balance_negative(self):
        """Тест расчета отрицательного баланса"""
        self.model.add_transaction("income", 5000.0, "Подработка", "")
        self.model.add_transaction("expense", 8000.0, "Развлечения", "")

        balance = self.model.get_balance()
        self.assertEqual(balance, -3000.0)

    def test_get_last_transactions(self):
        """Тест получения последних транзакций"""
        for i in range(15):
            self.model.add_transaction("expense", 100.0, "Еда", f"Транзакция {i}")

        last_10 = self.model.get_last_transactions(10)
        self.assertEqual(len(last_10), 10)

    def test_add_goal(self):
        """Тест добавления цели"""
        self.model.add_goal("Ноутбук", 50000.0)

        goals = self.model.data['goals']
        self.assertEqual(len(goals), 1)
        self.assertEqual(goals[0]['name'], 'Ноутбук')
        self.assertEqual(goals[0]['target'], 50000.0)

    def test_update_goal(self):
        """Тест обновления прогресса цели"""
        self.model.add_goal("Телефон", 30000.0)
        self.model.update_goal(0, 15000.0)

        goals = self.model.data['goals']
        self.assertEqual(goals[0]['current'], 15000.0)

    def test_get_monthly_expenses(self):
        """Тест получения расходов за текущий месяц"""
        self.model.add_transaction("expense", 1000.0, "Еда", "")
        self.model.add_transaction("expense", 500.0, "Транспорт", "")
        self.model.add_transaction("income", 15000.0, "Стипендия", "")

        expenses = self.model.get_monthly_expenses()
        self.assertIn("Еда", expenses)
        self.assertIn("Транспорт", expenses)
        self.assertEqual(expenses["Еда"], 1000.0)


class TestBudgetController(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_controller_budget.json"
        self.mock_view = MagicMock()
        self.controller = BudgetController(self.mock_view)
        self.model = BudgetModel(self.test_file)
        self.controller.set_model(self.model)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_income_transaction(self):
        """Тест добавления дохода через контроллер"""
        self.controller.add_transaction("income", 15000.0, "Стипендия", "")

        balance = self.model.get_balance()
        self.assertEqual(balance, 15000.0)
        self.mock_view.update_balance.assert_called()

    def test_add_expense_transaction(self):
        """Тест добавления расхода через контроллер"""
        self.controller.add_transaction("income", 10000.0, "Стипендия", "")
        self.controller.add_transaction("expense", 2000.0, "Еда", "")

        balance = self.model.get_balance()
        self.assertEqual(balance, 8000.0)

    def test_add_goal(self):
        """Тест добавления цели через контроллер"""
        self.controller.add_goal("Ноутбук", 50000.0)

        goals = self.model.data['goals']
        self.assertEqual(len(goals), 1)
        self.assertEqual(goals[0]['name'], 'Ноутбук')

    def test_update_goal(self):
        """Тест обновления цели через контроллер"""
        self.controller.add_goal("Телефон", 30000.0)
        self.controller.update_goal(0, 10000.0)

        goals = self.model.data['goals']
        self.assertEqual(goals[0]['current'], 10000.0)


if __name__ == '__main__':
    unittest.main()