from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QSpinBox, QPushButton, QMessageBox, QGroupBox, QLineEdit,
    QFrame
)
from PySide6.QtCore import Signal
from ui.components.chart_widget import InteractiveChartWidget


class CurrencyTrackerView(QWidget):
    update_requested = Signal(str, int)
    convert_requested = Signal(float, str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title_label = QLabel("Трекер валют")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")
        main_layout.addWidget(title_label)

        control_group = QGroupBox("Параметры")
        control_group.setStyleSheet("""
            QGroupBox {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                font-size: 14px;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        """)

        control_layout = QHBoxLayout()

        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["USD", "EUR", "CNY", "GBP", "JPY"])
        self.currency_combo.setStyleSheet("""
            QComboBox {
                background-color: #3d3d3d;
                color: #ffffff;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 5px;
                min-width: 100px;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        control_layout.addWidget(QLabel("Валюта:"))
        control_layout.addWidget(self.currency_combo)

        self.days_spin = QSpinBox()
        self.days_spin.setRange(7, 365)
        self.days_spin.setValue(30)
        self.days_spin.setStyleSheet("""
            QSpinBox {
                background-color: #3d3d3d;
                color: #ffffff;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
        """)
        control_layout.addWidget(QLabel("Дней:"))
        control_layout.addWidget(self.days_spin)

        self.update_btn = QPushButton("Обновить график")
        self.update_btn.clicked.connect(self.on_update_clicked)
        self.update_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1084d8;
            }
            QPushButton:pressed {
                background-color: #006cbd;
            }
            QPushButton:disabled {
                background-color: #555555;
            }
        """)
        control_layout.addWidget(self.update_btn)
        control_layout.addStretch()

        control_group.setLayout(control_layout)
        main_layout.addWidget(control_group)

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(10)

        self.current_value_card = self.create_stat_card("Текущий курс", "0.00 RUB", "#0078d7")
        self.change_card = self.create_stat_card("Изменение за день", "0.00%", "#0078d7")
        self.min_card = self.create_stat_card("Минимум за период", "0.00 RUB", "#0078d7")
        self.max_card = self.create_stat_card("Максимум за период", "0.00 RUB", "#0078d7")

        stats_layout.addWidget(self.current_value_card)
        stats_layout.addWidget(self.change_card)
        stats_layout.addWidget(self.min_card)
        stats_layout.addWidget(self.max_card)

        main_layout.addLayout(stats_layout)

        chart_group = QGroupBox("График динамики")
        chart_group.setStyleSheet("""
            QGroupBox {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                font-size: 14px;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        """)
        chart_layout = QVBoxLayout()
        self.chart = InteractiveChartWidget()
        chart_layout.addWidget(self.chart)
        chart_group.setLayout(chart_layout)
        main_layout.addWidget(chart_group)

        converter_group = QGroupBox("Калькулятор конвертации")
        converter_group.setStyleSheet("""
            QGroupBox {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                font-size: 14px;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        """)

        converter_layout = QHBoxLayout()

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Введите сумму")
        self.amount_input.setStyleSheet("""
            QLineEdit {
                background-color: #3d3d3d;
                color: #ffffff;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 8px;
                min-width: 150px;
            }
        """)
        converter_layout.addWidget(QLabel("Сумма:"))
        converter_layout.addWidget(self.amount_input)

        self.converter_currency_label = QLabel(self.currency_combo.currentText())
        self.converter_currency_label.setStyleSheet("font-weight: bold; min-width: 40px; color: #ffffff;")
        converter_layout.addWidget(self.converter_currency_label)

        self.currency_combo.currentTextChanged.connect(self.update_converter_currency_label)

        self.convert_btn = QPushButton("Конвертировать")
        self.convert_btn.clicked.connect(self.on_convert_clicked)
        self.convert_btn.setStyleSheet("""
            QPushButton {
                background-color: #00d084;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00e094;
            }
            QPushButton:pressed {
                background-color: #00b874;
            }
        """)
        converter_layout.addWidget(self.convert_btn)

        self.conversion_result_label = QLabel("Результат: 0.00 RUB (курс: 0.00)")
        self.conversion_result_label.setStyleSheet("font-size: 14px; color: #00d084; font-weight: bold;")
        converter_layout.addWidget(self.conversion_result_label)
        converter_layout.addStretch()

        converter_group.setLayout(converter_layout)
        main_layout.addWidget(converter_group)

        main_layout.addStretch()

    def create_stat_card(self, title: str, value: str, accent_color: str) -> QFrame:
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-left: 4px solid {accent_color};
                border-radius: 8px;
                padding: 15px;
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 12px; color: #888888;")
        layout.addWidget(title_label)

        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
        value_label.setObjectName("value_label")
        layout.addWidget(value_label)

        return card

    def update_converter_currency_label(self, text):
        self.converter_currency_label.setText(text)

    def on_update_clicked(self):
        currency = self.currency_combo.currentText()
        days = self.days_spin.value()
        self.update_requested.emit(currency, days)

    def on_convert_clicked(self):
        try:
            amount = float(self.amount_input.text())
            currency = self.currency_combo.currentText()
            self.convert_requested.emit(amount, currency)
        except ValueError:
            self.show_error("Введите корректное число для конвертации.")

    def update_chart(self, dates, values, currency_name, is_positive_change):
        self.chart.update_chart(dates, values, currency_name, is_positive_change)

    def update_stats(self, current_value, change_percent, min_value, max_value, currency_name):
        self.current_value_card.findChild(QLabel, "value_label").setText(
            f"{current_value:.2f} RUB"
        )

        change_text = f"{change_percent:+.2f}%"
        change_color = "#00d084" if change_percent >= 0 else "#ff4757"
        change_label = self.change_card.findChild(QLabel, "value_label")
        change_label.setText(change_text)
        change_label.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {change_color};")

        self.change_card.setStyleSheet(f"""
            QFrame {{
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-left: 4px solid {change_color};
                border-radius: 8px;
                padding: 15px;
            }}
        """)

        self.min_card.findChild(QLabel, "value_label").setText(f"{min_value:.2f} RUB")
        self.max_card.findChild(QLabel, "value_label").setText(f"{max_value:.2f} RUB")

    def update_conversion_result(self, result: float, rate: float):
        self.conversion_result_label.setText(
            f"Результат: {result:.2f} RUB (курс: {rate:.2f})"
        )

    def set_loading_state(self, is_loading: bool):
        self.update_btn.setEnabled(not is_loading)
        self.update_btn.setText("Загрузка..." if is_loading else "Обновить график")

    def show_error(self, message: str):
        QMessageBox.warning(self, "Ошибка", message)