from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QListWidget, QStackedWidget, QLabel
)
from PySide6.QtCore import Qt
from modules.currency_tracker.view import CurrencyTrackerView
from modules.currency_tracker.controller import CurrencyTrackerController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SuperApp v1.0")
        self.resize(1200, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Боковая панель навигации
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(220)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #1a1a1a;
                color: #ffffff;
                font-size: 14px;
                border: none;
            }
            QListWidget::item {
                padding: 18px 15px;
                border-bottom: 1px solid #2d2d2d;
            }
            QListWidget::item:selected {
                background-color: #0078d7;
                color: #ffffff;
            }
            QListWidget::item:hover {
                background-color: #2d2d2d;
            }
        """)
        self.sidebar.addItems([
            "Трекер валют",
            "Бюджет и накопления",
            "Утилита 3 (Заглушка)",
            "Утилита 4 (Заглушка)",
            "Утилита 5 (Заглушка)"
        ])
        self.sidebar.currentRowChanged.connect(self.switch_page)
        main_layout.addWidget(self.sidebar)

        # Область контента
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: #252525;")

        # Страница 0: Трекер валют
        self.tracker_view = CurrencyTrackerView()
        self.tracker_controller = CurrencyTrackerController(self.tracker_view)
        self.stack.addWidget(self.tracker_view)

        # Страница 1: Бюджет и накопления
        from modules.budget_manager.view import BudgetView
        from modules.budget_manager.controller import BudgetController
        from modules.budget_manager.models import BudgetModel

        self.budget_view = BudgetView()
        self.budget_controller = BudgetController(self.budget_view)
        self.budget_model = BudgetModel()

        self.budget_view.set_controller(self.budget_controller)
        self.budget_controller.set_model(self.budget_model)

        self.stack.addWidget(self.budget_view)

        # Страницы 2-4: Заглушки
        for i in range(2, 5):
            stub = QLabel(
                f"Утилита {i + 1} находится в разработке.\n\nЗдесь будет новый модуль SuperApp.",
                alignment=Qt.AlignCenter
            )
            stub.setStyleSheet("font-size: 18px; color: #888888;")
            self.stack.addWidget(stub)

        main_layout.addWidget(self.stack)

        # Загружаем данные при старте
        self.tracker_controller.load_data("USD", 30)

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)