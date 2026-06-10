from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QDoubleSpinBox, QLineEdit, QGroupBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QProgressBar, QTabWidget, QMessageBox,
    QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class BudgetView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = None
        self.init_ui()

    def set_controller(self, controller):
        self.controller = controller

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        title = QLabel("Бюджет и накопления")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab { background: #333; color: white; padding: 12px 25px; border: none; font-size: 14px; }
            QTabBar::tab:selected { background: #0078d7; }
            QTabWidget::pane { background: #2b2b2b; border: 1px solid #444; border-radius: 8px; }
        """)
        layout.addWidget(self.tabs)

        self.create_transactions_tab()
        self.create_goals_tab()

    def create_transactions_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        balance_group = QGroupBox("Текущий баланс")
        balance_group.setStyleSheet("color: white; font-size: 14px;")
        b_layout = QHBoxLayout()
        self.balance_label = QLabel("0.00 RUB")
        self.balance_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #00d084;")
        b_layout.addWidget(self.balance_label)
        b_layout.addStretch()
        balance_group.setLayout(b_layout)
        layout.addWidget(balance_group)

        form_group = QGroupBox("Добавить операцию")
        form_group.setStyleSheet("color: white; font-size: 14px;")
        f_layout = QVBoxLayout()

        row1 = QHBoxLayout()
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Расход", "Доход"])
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        row1.addWidget(QLabel("Тип:"))
        row1.addWidget(self.type_combo)

        self.category_combo = QComboBox()
        self.category_combo.addItems(["Еда", "Транспорт", "Развлечения", "Учеба", "Другое"])
        row1.addWidget(QLabel("Категория:"))
        row1.addWidget(self.category_combo)
        f_layout.addLayout(row1)

        row2 = QHBoxLayout()
        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0, 1000000)
        self.amount_spin.setSuffix(" RUB")
        row2.addWidget(QLabel("Сумма:"))
        row2.addWidget(self.amount_spin)

        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Описание")
        row2.addWidget(self.desc_input)
        f_layout.addLayout(row2)

        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self.on_add_transaction)
        add_btn.setStyleSheet("background: #0078d7; color: white; padding: 8px; border-radius: 4px; font-weight: bold;")
        add_btn.setMinimumHeight(35)
        f_layout.addWidget(add_btn)

        form_group.setLayout(f_layout)
        layout.addWidget(form_group)

        scroll_area = QWidget()
        scroll_layout = QVBoxLayout(scroll_area)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(10)

        table_group = QGroupBox("Последние 10 операций")
        table_group.setStyleSheet("color: white; font-size: 14px;")
        t_layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Дата", "Тип", "Категория", "Сумма", ""])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("background: #1e1e1e; color: white; gridline-color: #444;")
        self.table.setMinimumHeight(250)
        t_layout.addWidget(self.table)
        table_group.setLayout(t_layout)
        scroll_layout.addWidget(table_group)

        chart_group = QGroupBox("Расходы по категориям за месяц")
        chart_group.setStyleSheet("color: white; font-size: 14px;")
        c_layout = QVBoxLayout()

        self.figure = Figure(figsize=(6, 4), facecolor='#1e1e1e')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(300)
        c_layout.addWidget(self.canvas)

        chart_group.setLayout(c_layout)
        scroll_layout.addWidget(chart_group)
        scroll_layout.addStretch()

        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True)
        main_scroll.setWidget(scroll_area)
        main_scroll.setStyleSheet("border: none; background: transparent;")

        layout.addWidget(main_scroll)

        self.tabs.addTab(tab, "Операции")

    def create_goals_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)

        form_group = QGroupBox("Новая цель")
        form_group.setStyleSheet("color: white; font-size: 14px;")
        f_layout = QHBoxLayout()

        self.goal_name_input = QLineEdit()
        self.goal_name_input.setPlaceholderText("Название (например, Ноутбук)")
        f_layout.addWidget(self.goal_name_input)

        self.goal_amount_spin = QDoubleSpinBox()
        self.goal_amount_spin.setRange(1, 1000000)
        self.goal_amount_spin.setSuffix(" RUB")
        f_layout.addWidget(self.goal_amount_spin)

        add_btn = QPushButton("Добавить цель")
        add_btn.clicked.connect(self.on_add_goal)
        add_btn.setStyleSheet("background: #00d084; color: white; padding: 8px; border-radius: 4px;")
        f_layout.addWidget(add_btn)

        form_group.setLayout(f_layout)
        layout.addWidget(form_group)

        self.goals_layout = QVBoxLayout()
        layout.addLayout(self.goals_layout)
        layout.addStretch()

        self.tabs.addTab(tab, "Цели")

    def on_type_changed(self, text):
        self.category_combo.clear()
        if text == "Доход":
            self.category_combo.addItems(["Стипендия", "Подработка", "Подарки", "Другое"])
        else:
            self.category_combo.addItems(["Еда", "Транспорт", "Развлечения", "Учеба", "Другое"])

    def on_add_transaction(self):
        if self.controller:
            t_type = "income" if self.type_combo.currentText() == "Доход" else "expense"
            amount = self.amount_spin.value()
            category = self.category_combo.currentText()
            desc = self.desc_input.text() or "-"
            self.controller.add_transaction(t_type, amount, category, desc)
            self.amount_spin.setValue(0)
            self.desc_input.clear()

    def on_delete_transaction(self, trans_id):
        if self.controller:
            reply = QMessageBox.question(
                self,
                'Подтверждение',
                'Удалить эту транзакцию?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.controller.delete_transaction(trans_id)

    def on_add_goal(self):
        if self.controller:
            name = self.goal_name_input.text()
            target = self.goal_amount_spin.value()
            if not name:
                QMessageBox.warning(self, "Ошибка", "Введите название цели")
                return
            self.controller.add_goal(name, target)
            self.goal_name_input.clear()
            self.goal_amount_spin.setValue(0)

    def on_delete_goal(self, goal_id):
        if self.controller:
            reply = QMessageBox.question(
                self,
                'Подтверждение',
                'Удалить эту цель?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.controller.delete_goal(goal_id)

    def update_balance(self, balance):
        self.balance_label.setText(f"{balance:.2f} RUB")
        color = "#00d084" if balance >= 0 else "#ff4757"
        self.balance_label.setStyleSheet(f"font-size: 32px; font-weight: bold; color: {color};")

    def update_transactions_table(self, transactions):
        self.table.setRowCount(len(transactions))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Дата", "Тип", "Категория", "Сумма", ""])

        for i, t in enumerate(transactions):
            self.table.setItem(i, 0, QTableWidgetItem(t['date']))
            type_text = "Доход" if t['type'] == 'income' else "Расход"
            type_item = QTableWidgetItem(type_text)
            type_item.setForeground(QColor("#00d084" if t['type'] == 'income' else "#ff4757"))
            self.table.setItem(i, 1, type_item)
            self.table.setItem(i, 2, QTableWidgetItem(t['category']))

            amount_item = QTableWidgetItem(f"{t['amount']:.2f}")
            amount_item.setForeground(QColor("#00d084" if t['type'] == 'income' else "#ff4757"))
            self.table.setItem(i, 3, amount_item)

            delete_btn = QPushButton("Удалить")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff4757;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 5px 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #ff6b7a;
                }
            """)
            # Передаем ID транзакции, а не индекс
            delete_btn.clicked.connect(lambda checked, tid=t['id']: self.on_delete_transaction(tid))

            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.addWidget(delete_btn)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(i, 4, widget)

        self.table.setColumnWidth(4, 80)

    def update_pie_chart(self, expenses):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if not expenses:
            ax.text(0.5, 0.5, 'Нет расходов за этот месяц',
                    ha='center', va='center', color='white', fontsize=12)
            ax.set_xticks([])
            ax.set_yticks([])
        else:
            labels = list(expenses.keys())
            sizes = list(expenses.values())
            colors = ['#ff4757', '#2ed573', '#1e90ff', '#ffa502', '#3742fa']

            wedges, texts, autotexts = ax.pie(
                sizes, labels=labels, autopct='%1.1f%%',
                colors=colors[:len(labels)], startangle=90,
                textprops={'color': 'white', 'fontsize': 9}
            )
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')

        self.figure.tight_layout()
        self.canvas.draw()

    def update_goals_list(self, goals):
        while self.goals_layout.count():
            item = self.goals_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for i, goal in enumerate(goals):
            widget = QWidget()
            widget.setStyleSheet("background: #2d2d2d; border-radius: 6px; padding: 10px; margin: 5px;")
            layout = QVBoxLayout(widget)

            header = QHBoxLayout()
            header.addWidget(QLabel(f"<b style='color:white'>{goal['name']}</b>"))
            header.addWidget(QLabel(f"<span style='color:#aaa'>{goal['current']:.0f} / {goal['target']:.0f} RUB</span>"))
            header.addStretch()

            delete_btn = QPushButton("Удалить цель")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff4757;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 5px 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #ff6b7a;
                }
            """)
            # Передаем ID цели, а не индекс
            delete_btn.clicked.connect(lambda checked, gid=goal['id']: self.on_delete_goal(gid))
            header.addWidget(delete_btn)

            layout.addLayout(header)

            progress = QProgressBar()
            progress.setMaximum(100)
            percent = int((goal['current'] / goal['target']) * 100) if goal['target'] > 0 else 0
            progress.setValue(min(percent, 100))
            progress.setStyleSheet("""
                QProgressBar { background: #1e1e1e; border-radius: 4px; text-align: center; color: white; }
                QProgressBar::chunk { background: #0078d7; border-radius: 4px; }
            """)
            layout.addWidget(progress)

            row = QHBoxLayout()
            spin = QDoubleSpinBox()
            spin.setRange(0, goal['target'])
            spin.setValue(goal['current'])
            spin.setSuffix(" RUB")
            row.addWidget(QLabel("Накоплено:", styleSheet="color: white;"))
            row.addWidget(spin)

            btn = QPushButton("Сохранить")
            # Передаем ID цели
            btn.clicked.connect(lambda checked, gid=goal['id'], s=spin: self.controller.update_goal(gid, s.value()))
            btn.setStyleSheet("background: #0078d7; color: white; padding: 5px; border-radius: 4px;")
            row.addWidget(btn)
            row.addStretch()
            layout.addLayout(row)

            self.goals_layout.addWidget(widget)