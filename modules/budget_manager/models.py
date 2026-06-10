import json
import os
from datetime import datetime


class BudgetModel:
    def __init__(self, filename='budget_data.json'):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)

            # Добавляем id к старым транзакциям, если их нет
            for i, trans in enumerate(loaded_data.get('transactions', [])):
                if 'id' not in trans:
                    trans['id'] = i + 1

            # Добавляем id к старым целям, если их нет
            for i, goal in enumerate(loaded_data.get('goals', [])):
                if 'id' not in goal:
                    goal['id'] = i + 1

            # Сохраняем обновленные данные
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(loaded_data, f, ensure_ascii=False, indent=4)

            return loaded_data
        return {'transactions': [], 'goals': []}

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def add_transaction(self, t_type, amount, category, desc):
        transaction = {
            'id': len(self.data['transactions']) + 1,
            'type': t_type,
            'amount': float(amount),
            'category': category,
            'desc': desc,
            'date': datetime.now().strftime('%d.%m.%Y %H:%M')
        }
        self.data['transactions'].append(transaction)
        self.save_data()

    def delete_transaction_by_id(self, trans_id):
        for i, t in enumerate(self.data['transactions']):
            if t['id'] == trans_id:
                self.data['transactions'].pop(i)
                self.save_data()
                return True
        return False

    def get_balance(self):
        balance = 0.0
        for t in self.data['transactions']:
            if t['type'] == 'income':
                balance += t['amount']
            else:
                balance -= t['amount']
        return balance

    def get_last_transactions(self, limit=10):
        return self.data['transactions'][-limit:][::-1]

    def add_goal(self, name, target):
        self.data['goals'].append({
            'id': len(self.data['goals']) + 1,
            'name': name,
            'target': float(target),
            'current': 0.0
        })
        self.save_data()

    def delete_goal_by_id(self, goal_id):
        for i, g in enumerate(self.data['goals']):
            if g['id'] == goal_id:
                self.data['goals'].pop(i)
                self.save_data()
                return True
        return False

    def update_goal_by_id(self, goal_id, amount):
        for g in self.data['goals']:
            if g['id'] == goal_id:
                g['current'] = float(amount)
                self.save_data()
                return True
        return False

    def get_monthly_expenses(self):
        current_month = datetime.now().strftime('%m.%Y')
        expenses = {}
        for t in self.data['transactions']:
            if t['type'] == 'expense' and t['date'][3:10] == current_month:
                cat = t['category']
                expenses[cat] = expenses.get(cat, 0.0) + t['amount']
        return expenses