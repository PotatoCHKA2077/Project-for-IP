import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QStackedWidget


class StackedWindows(QStackedWidget):  # Класс, собирающий все окна в одно.
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('доп файлы/icon.ico'))
        self.setWindowTitle('Зубрилка')
        self.setMinimumSize(560, 300)
        self.resize(560, 300)


def add_widget(widget):  # Функция для добавления окна в StackedWindows.
    stacked_windows.addWidget(widget)


def open_window(i):  # Функция для открытия определенного окна из StackedWindows.
    stacked_windows.setCurrentIndex(i)


app = QApplication(sys.argv)
stacked_windows = StackedWindows()
