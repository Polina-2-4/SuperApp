class BudgetController:
    def __init__(self, view):
        self.view = view
        self.model = None

    def set_model(self, model):
        self.model = model
        self.refresh_ui()

    def add_transaction(self, t_type, amount, category, desc):
        if self.model:
            self.model.add_transaction(t_type, amount, category, desc)
            self.refresh_ui()

    def delete_transaction(self, trans_id):
        if self.model:
            self.model.delete_transaction_by_id(trans_id)
            self.refresh_ui()

    def add_goal(self, name, target):
        if self.model:
            self.model.add_goal(name, target)
            self.refresh_ui()

    def delete_goal(self, goal_id):
        if self.model:
            self.model.delete_goal_by_id(goal_id)
            self.refresh_ui()

    def update_goal(self, goal_id, amount):
        if self.model:
            self.model.update_goal_by_id(goal_id, amount)
            self.refresh_ui()

    def refresh_ui(self):
        if self.model:
            balance = self.model.get_balance()
            transactions = self.model.get_last_transactions(10)
            expenses = self.model.get_monthly_expenses()
            goals = self.model.data['goals']

            self.view.update_balance(balance)
            self.view.update_transactions_table(transactions)
            self.view.update_pie_chart(expenses)
            self.view.update_goals_list(goals)