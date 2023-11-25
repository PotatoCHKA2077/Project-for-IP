import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, QFileDialog, QInputDialog, QLabel, QPushButton,
                             QColorDialog)
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageDraw
from games import *
from stacked_windows import add_widget, open_window, stacked_windows


class StartWindow(QMainWindow):  # Класс реализующий стартовое окно
    def __init__(self):
        super().__init__()
        loadUi('доп файлы/start window.ui', self)
        self.menu_btn.clicked.connect(self.open_menu)
        self.instruct_btn.clicked.connect(self.open_instruct)
        self.cod_btn.clicked.connect(self.cod_writing)
        self.painter = Painter()
        self.cat = Cat()
        self.dog = Dog()

    @staticmethod
    def open_menu():  # Метод для открытия окна выбора режимов.
        message = QMessageBox()
        message.setText('Когда откроется следующее окно, пожалуйста выберите файл с нужной темой.')
        message.setInformativeText('Можно выбрать файлы из предложенных сразу, или сделать самому и выбрать его.')
        message.setWindowTitle('Пожалуйста выберите файл!')
        message.exec()
        file_name = QFileDialog.getOpenFileName(stacked_windows, 'Выбрать файл', 'доп файлы', 'CSV файл (*.csv)')[0]
        menu = MenuWindow(file_name)
        add_widget(menu)
        open_window(8)

    @staticmethod
    def open_instruct():  # Метод для открытия руководства по пользованию.
        stacked_windows.resize(470, 500)
        open_window(1)
    
    def cod_writing(self):  # Метод для ввода секретных кодов.
        cod, ok_pressed = QInputDialog.getText(self, 'Введите код', 'Здесь вы можете ввести секретный код.')
        if ok_pressed:
            if cod == 'secret':
                self.painter.show()
                message = QMessageBox()
                message.setText('Поздравляем, вы нашли секретное окно!')
                message.setInformativeText('Здесь вы можете нарисовать себе тортик'
                                           ' или еще что-нибудь, в честь вашего открытия. Рисунок сохраняется '
                                           'автоматически в папку "доп файлы", но только последняя его версия.'
                                           ' Только никому не говорите о нашем маленьком секрете!🤐🤐🤐')
                message.setWindowTitle('🤐🤐🤐')
                message.exec()
            if cod == 'I love cats':
                self.cat.show()
                message = QMessageBox()
                message.setText('О, вы тоже любите котов? Ну конечно, иначе бы вы не ввели этот секретный код! '
                                'Ну раз так, то вот вам картинка милого котика.')
                message.exec()
            if cod == 'I love dogs':
                self.dog.show()
                message = QMessageBox()
                message.setText('О, вы тоже любите собак? Ну конечно, иначе бы вы не ввели этот секретный код! '
                                'Ну раз так, то вот вам картинка милой собачки.')
                message.exec()


class InstructWindow(QMainWindow):  # Класс реализующий окно с руководством по пользованию.
    def __init__(self):
        super().__init__()
        loadUi('доп файлы/instruct window.ui', self)
        with open('доп файлы/руководство.txt', 'rt', encoding='utf8') as instruct:
            self.instruction.setText(instruct.read())
        self.exit_btn.clicked.connect(self.exit)

    @staticmethod
    def exit():
        stacked_windows.resize(560, 300)
        open_window(0)


class Painter(QMainWindow):  # Класс, реализующий секретную рисовалку.
    def __init__(self):
        super().__init__()
        self.resize(500, 560)
        self.setWindowTitle('Секретное окно')
        self.img_name = 'доп файлы/ваш рисунок.png'
        self.color = 'red'
        self.img = Image.new('RGB', (500, 500), (255, 255, 255))
        self.img.save(self.img_name, 'PNG')
        self.pixmap = QPixmap(self.img_name)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(500, 500)
        self.image.setPixmap(self.pixmap)
        self.color_btn = QPushButton(self)
        self.color_btn.move(0, 500)
        self.color_btn.resize(500, 30)
        self.color_btn.setText('Здесь можно выбрать цвет')
        self.eraser = QPushButton(self)
        self.eraser.move(0, 530)
        self.eraser.resize(500, 30)
        self.eraser.setText('Ластик')
        self.need_eraser = False
        self.color_btn.clicked.connect(self.color_change)
        self.eraser.clicked.connect(self.erasering)
        self.point = None

    def color_change(self):  # Метод для выбора цвета.
        color = QColorDialog().getColor()
        if color.isValid():
            self.color = color.name()

    def erasering(self):  # Метод для выбора ластика.
        if self.eraser.text() == 'Ластик':
            self.need_eraser = True
            self.eraser.setText('Продолжить рисовать')
        else:
            self.need_eraser = False
            self.eraser.setText('Ластик')

    def mouseMoveEvent(self, event):
        self.point = (event.x(), event.y())
        self.update()
    
    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.point:
            return
        if not self.need_eraser:
            img = Image.open(self.img_name)
            draw = ImageDraw.Draw(img)
            draw.rectangle((self.point[0] - 1, self.point[1] - 1, self.point[0] + 1, self.point[1] + 1),
                           fill=self.color)
            img.save(self.img_name, 'PNG')
            self.pixmap = QPixmap(self.img_name)
            self.image.setPixmap(self.pixmap)
        else:
            img = Image.open(self.img_name)
            draw = ImageDraw.Draw(img)
            draw.rectangle((self.point[0] - 3, self.point[1] - 3, self.point[0] + 3, self.point[1] + 3), fill='white')
            img.save(self.img_name, 'PNG')
            self.pixmap = QPixmap(self.img_name)
            self.image.setPixmap(self.pixmap)


class Cat(QMainWindow):  # Класс, реализующий секрет с котиком.
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self.setWindowTitle('Cat')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(500, 500)
        self.pixmap = QPixmap('доп файлы/cat.png')
        self.image.setPixmap(self.pixmap)


class Dog(QMainWindow):  # Класс, реализующий секрет с собачкой
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self.setWindowTitle('Dog')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(500, 500)
        self.pixmap = QPixmap('доп файлы/dog.png')
        self.image.setPixmap(self.pixmap)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    start = StartWindow()
    add_widget(start)
    instrust = InstructWindow()
    add_widget(instrust)
    open_window(0)
    stacked_windows.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
