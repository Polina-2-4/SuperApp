import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt


class InteractiveChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground("#1e1e1e")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setLabel('left', 'Курс (RUB)', color='#ffffff', size='12pt')
        self.plot_widget.setLabel('bottom', 'Дата', color='#ffffff', size='12pt')
        self.plot_widget.addLegend()

        # Настройка осей
        axis_color = '#888888'
        self.plot_widget.getAxis('left').setPen(pg.mkPen(color=axis_color))
        self.plot_widget.getAxis('bottom').setPen(pg.mkPen(color=axis_color))
        self.plot_widget.getAxis('left').setTextPen(pg.mkPen(color=axis_color))
        self.plot_widget.getAxis('bottom').setTextPen(pg.mkPen(color=axis_color))

        self.layout.addWidget(self.plot_widget)
        self.line = None
        self.dates = []

        # Добавляем Crosshair для отображения значений при наведении
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('#ffffff', width=1, style=Qt.DashLine))
        self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('#ffffff', width=1, style=Qt.DashLine))
        self.plot_widget.addItem(self.vLine, ignoreBounds=True)
        self.plot_widget.addItem(self.hLine, ignoreBounds=True)

        # Label для отображения значений
        self.label = pg.TextItem(anchor=(0, 1), color='#ffffff', fill=pg.mkColor(50, 50, 50, 200))
        self.label.hide()
        self.plot_widget.addItem(self.label)

        # Подключаем сигнал наведения мыши
        self.plot_widget.scene().sigMouseMoved.connect(self.mouseMoved)

    def mouseMoved(self, evt):
        """Обработка движения мыши для отображения значений"""
        pos = evt
        if self.plot_widget.sceneBoundingRect().contains(pos):
            mousePoint = self.plot_widget.plotItem.vb.mapSceneToView(pos)
            index = int(mousePoint.x())

            if 0 <= index < len(self.dates) and self.line is not None:
                data = self.line.getData()
                if data[1] is not None and index < len(data[1]):
                    value = data[1][index]
                    date = self.dates[index]

                    # Показываем label с информацией
                    self.label.setText(f"{date}\nКурс: {value:.2f} RUB")
                    self.label.setPos(mousePoint.x(), mousePoint.y())
                    self.label.show()

                    # Двигаем линии перекрестия
                    self.vLine.setPos(mousePoint.x())
                    self.hLine.setPos(mousePoint.y())
            else:
                self.label.hide()

    def update_chart(self, dates, values, currency_name, is_positive_change=True):
        """Обновляет данные на графике"""
        self.plot_widget.clear()

        # Пересоздаем элементы после clear
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('#ffffff', width=1, style=Qt.DashLine))
        self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('#ffffff', width=1, style=Qt.DashLine))
        self.plot_widget.addItem(self.vLine, ignoreBounds=True)
        self.plot_widget.addItem(self.hLine, ignoreBounds=True)

        self.label = pg.TextItem(anchor=(0, 1), color='#ffffff', fill=pg.mkColor(50, 50, 50, 200))
        self.label.hide()
        self.plot_widget.addItem(self.label)

        self.dates = dates

        if not dates or not values:
            return

        x_ticks = [(i, date) for i, date in enumerate(dates)]
        self.plot_widget.getAxis('bottom').setTicks([x_ticks])

        # Цвет линии зависит от тренда
        color = '#00d084' if is_positive_change else '#ff4757'

        self.line = self.plot_widget.plot(
            list(range(len(values))),
            values,
            pen=pg.mkPen(color=color, width=2),
            name=currency_name,
            symbol='o',
            symbolBrush=color,
            symbolSize=5,
            symbolPen=pg.mkPen(color='#1e1e1e', width=1)
        )

        self.plot_widget.autoRange()