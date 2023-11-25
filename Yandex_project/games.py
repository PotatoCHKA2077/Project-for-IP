import csv
import sqlite3
from random import shuffle, sample
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from stacked_windows import open_window, add_widget, stacked_windows

    
class MenuWindow(QMainWindow):  # Класс, реализующий окно выбора режимов.
    def __init__(self, file_name):
        super().__init__()
        self.file = file_name
        self.initUI()

    def initUI(self):
        uic.loadUi('доп файлы/menu window.ui', self)
        card = CardLearning(self.file)
        add_widget(card)
        test = Test(self.file)
        add_widget(test)
        writing = Writing(self.file)
        add_widget(writing)
        control_test = ControlTest(self.file)
        add_widget(control_test)
        control_writing = ControlWriting(self.file)
        add_widget(control_writing)
        end_control = EndControl()
        add_widget(end_control)
        self.card_btn.clicked.connect(self.open_card_learning)
        self.back_btn.clicked.connect(self.close_menu)
        self.test_btn.clicked.connect(self.open_test)
        self.writing_btn.clicked.connect(self.open_writing)
        self.control_work_btn.clicked.connect(self.open_control_work)

    @staticmethod
    def close_menu():  # Метод для возвращения на стартовое окно.
        open_window(0)

    @staticmethod
    def open_card_learning():  # Метод для открытия режима карточек.
        open_window(2)

    @staticmethod
    def open_test():  # Метод для открытия режима теста.
        open_window(3)

    @staticmethod
    def open_writing():  # Метод для открытия режима записи.
        open_window(4)

    @staticmethod
    def open_control_work():  # Метод для открытия контрольной.
        open_window(5)

    def open_data(self):  # Метод для открытия csv файла с темой.
        with open(self.file, encoding='utf8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            self.data = {x[0]: [x[1], x[2]] for x in reader}
            self.true_answers = {x: self.data[x][0] for x in self.data}
            self.all_questions = list(self.data.keys())
            self.questions = sample(self.all_questions, 20)
            shuffle(self.all_questions)


class CardLearning(MenuWindow):  # Класс, реализующий режим карточек.
    def __init__(self, file_name):
        super().__init__(file_name)
        self.file = file_name
        self.initUI()

    def initUI(self):
        uic.loadUi('доп файлы/card window.ui', self)
        self.card.setText('Нажмите "далее" чтобы начать')
        self.card.clicked.connect(self.turn_over)
        self.next_btn.clicked.connect(self.next)
        self.end_btn.clicked.connect(self.close_window)
        self.open_data()

    def turn_over(self):  # Метод, реализующий "переворачивание карточки".
        card_text = self.card.text()
        for k, v in self.true_answers.items():
            if card_text == k:  # Проверка на ключ.
                self.card.setText(v)
                break
            elif card_text == v:  # Проверка на значение.
                self.card.setText(k)
                break

    def next(self):  # Метод, реализующий переход к следующей карточке.
        self.open_data()
        card_text = self.card.text()
        if card_text in self.true_answers.values():
            for k, v in self.true_answers.items():
                if card_text == v:  # Проверка на значение.
                    self.card.setText(k)
                    break
        try:
            self.card.setText(self.all_questions[self.all_questions.index(self.card.text()) + 1])
        except IndexError:
            message_box = QMessageBox()  # Всплывающее окно, оповещающее о том, что все карточки пройдены.
            message_box.setWindowTitle('Карточки закончились!')
            message_box.setText('Поздравляем! Вы прошли все карточки!')
            message_box.exec()
            self.card.setText(self.all_questions[0])
        except ValueError:
            self.card.setText(self.all_questions[0])

    @staticmethod
    def close_window():  # Метод, реализующий закрытие окна с карточками.
        open_window(8)


class Test(MenuWindow):  # Класс, реализующий режим теста.
    def __init__(self, file_name):
        super().__init__(file_name)
        self.file = file_name
        self.initUI()

    def initUI(self):
        uic.loadUi('доп файлы/test window.ui', self)
        self.open_data()
        for i in self.buttonGroup_answers.buttons():
            i.clicked.connect(self.checking)
        self.question.setText(self.questions[0])
        self.questioning()
        self.next_btn.clicked.connect(self.next)

    def questioning(self):  # Метод, реализующий разброс вариантов ответов по Radio Buttons.
        self.answering()
        self.answer1.setText(self.answers[0])
        self.answer2.setText(self.answers[1])
        self.answer3.setText(self.answers[2])
        self.answer4.setText(self.answers[3])
        for btn in self.buttonGroup_answers.buttons():
            btn.show()
            if btn.text() == '':
                btn.hide()

    def checking(self):  # Метод, реализующий проверку ответа.
        if self.sender().text() == self.data[self.question.text()][0]:
            self.statusbar.showMessage('Ответ правильный. Нажмите "Далее", чтобы продолжить')
        else:
            self.statusbar.showMessage('Ответ неправильный. Попробуйте снова.')

    def next(self):  # Метод, реализующий переход к следующему вопросу.
        try:
            self.statusbar.showMessage('')
            self.question.setText(self.questions[self.questions.index(self.question.text()) + 1])
            self.questioning()
        except IndexError:
            message_box = QMessageBox()  # Всплывающее окно, оповещающее об окончании теста.
            message_box.setWindowTitle('Тест закончился!')
            message_box.setText('Поздравляем! Вы прошли весь тест!')
            message_box.exec()
            open_window(8)
            self.questions = sample(self.all_questions, 20)
            self.question.setText(self.questions[0])
            self.questioning()

    def answering(self):
        without_true = self.data[self.question.text()][1].split(';')
        while len(without_true) < 3:
            without_true.append('')
        self.answers = sample(without_true, 3) + [self.data[self.question.text()][0]]
        shuffle(self.answers)
        self.answers.sort(key=lambda x: len(x), reverse=True)


class Writing(MenuWindow):  # Класс, реализующий режим записи.
    def __init__(self, file_name):
        super().__init__(file_name)
        self.file = file_name
        self.initUI()

    def initUI(self):
        uic.loadUi('доп файлы/writing window.ui', self)
        self.open_data()
        self.question.setText(self.questions[0])
        self.next_btn.clicked.connect(self.check_and_next)
        self.user_answer.returnPressed.connect(self.check_and_next)

    def check_and_next(self):  # Метод, реализующий проверку ответа и переход к следующему вопросу.
        if self.next_btn.text() == 'Проверить ответ':  # Проверка ответа.
            if self.user_answer.text() == self.data[self.question.text()][0]:
                self.statusbar.showMessage('Ответ правильный. Нажмите "Далее", чтобы продолжить')
                self.next_btn.setText('Далее')
            else:
                self.statusbar.showMessage('Ответ неправильный. Попробуйте снова.')
        else:  # Переход к следующему вопросу.
            try:
                self.statusbar.showMessage('')
                self.question.setText(self.questions[self.questions.index(self.question.text()) + 1])
                self.user_answer.setText('')
                self.next_btn.setText('Проверить ответ')
            except IndexError:
                message_box = QMessageBox()  # Всплывающее окно, оповещающее об окончании режима записи.
                message_box.setWindowTitle('Задание закончилось!')
                message_box.setText('Поздравляем! Вы прошли всё задание!')
                message_box.exec()
                open_window(8)
                self.questions = sample(self.all_questions, 20)
                self.question.setText(self.questions[0])
                self.user_answer.setText('')
                self.next_btn.setText('Проверить ответ')


class ControlTest(MenuWindow):  # Класс, реализующий тестовую часть контрольной.
    def __init__(self, file_name):
        super().__init__(file_name)
        self.file = file_name
        self.initUI()

    def initUI(self):
        uic.loadUi('доп файлы/test window.ui', self)
        self.statusbar.showMessage('')
        self.open_data()
        self.answer = ''
        with sqlite3.connect('доп файлы/control answers.db') as con:
            cur = con.cursor()
            cur.execute("""delete from controltest""")
            con.commit()  # ↑ Очищаем таблицу с ответами на тестовую часть, на случай если она не пуста.
        self.question.setText(self.questions[0])
        self.questioning()
        self.next_btn.clicked.connect(self.next)

    def questioning(self):  # Метод, реализующий разброс вариантов ответов по Radio Buttons.
        self.answering()
        self.answer1.setText(self.answers[0])
        self.answer2.setText(self.answers[1])
        self.answer3.setText(self.answers[2])
        self.answer4.setText(self.answers[3])
        for btn in self.buttonGroup_answers.buttons():
            btn.show()
            if btn.text() == '':
                btn.hide()

    def next(self):  # Метод, реализующий переход к следующему вопросу и запись ответа в специальную базу данных.
        try:
            for i in self.buttonGroup_answers.buttons():
                if i.isChecked():
                    self.answer = i.text()
                    break
            question = self.question.text()
            user_answer = self.answer
            true_answer = self.data[self.question.text()][0]
            val = (question, user_answer, true_answer)
            with sqlite3.connect('доп файлы/control answers.db') as con:
                cur = con.cursor()
                cur.execute("""insert into controltest values(?,?,?)""", val).fetchall()  # Запись в базу данных.
                con.commit()
            self.question.setText(self.questions[self.questions.index(self.question.text()) + 1])
            self.questioning()  # ↑ Переход к следующему вопросу.
        except IndexError:
            open_window(6)  # Переход к письменной части контрольной.
            self.questions = sample(self.all_questions, 20)
            self.question.setText(self.questions[0])
            self.questioning()

    def answering(self):
        without_true = self.data[self.question.text()][1].split(';')
        while len(without_true) < 3:
            without_true.append('')
        self.answers = sample(without_true, 3) + [self.data[self.question.text()][0]]
        shuffle(self.answers)


class ControlWriting(MenuWindow):  # Класс, реализующий письменную часть контрольной.
    def __init__(self, file_name):
        super().__init__(file_name)
        self.file = file_name
        self.answer = ''
        self.initUI()

    def initUI(self):
        uic.loadUi('доп файлы/writing window.ui', self)
        self.next_btn.setText('Далее')
        self.open_data()
        with sqlite3.connect('доп файлы/control answers.db') as con:
            cur = con.cursor()
            cur.execute("""delete from controlwriting""")
            con.commit()  # ↑ Очищаем таблицу с ответами на тестовую часть, на случай если она не пуста.
        self.question.setText(self.questions[0])
        self.next_btn.clicked.connect(self.next)
        self.user_answer.returnPressed.connect(self.next)
        self.statusbar.showMessage('')

    def next(self):  # Метод, реализующий переход к следующему вопросу и запись ответа в специальную базу данных.
        try:
            self.answer = self.user_answer.text()
            question = self.question.text()
            true_answer = self.data[self.question.text()][0]
            val = (question, self.answer, true_answer)
            with sqlite3.connect('доп файлы/control answers.db') as con:
                cur = con.cursor()
                cur.execute("""insert into controlwriting values(?,?,?)""", val).fetchall()  # Запись в базу данных
                con.commit()
            self.question.setText(self.questions[self.questions.index(self.question.text()) + 1])
            self.user_answer.setText('')  # ↑ Переход к следующему вопросу.
        except IndexError:
            open_window(7)
            self.questions = sample(self.all_questions, 20)
            self.question.setText(self.questions[0])
            self.user_answer.setText('')


class EndControl(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('доп файлы/control_end window.ui', self)
        self.get_result_btn.clicked.connect(self.open_results)
        self.exit_btn.clicked.connect(self.close_window)

    @staticmethod
    def close_window():  # Метод, реализующий возвращения в меню выбора режимов.
        open_window(2)

    @staticmethod
    def open_results():
        results = ControlResults()
        add_widget(results)
        open_window(9)


class ControlResults(QMainWindow):  # Класс, реализующий окно с результатами.
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('доп файлы/control_results window.ui', self)
        stacked_windows.resize(510, 545)
        with sqlite3.connect('доп файлы/control answers.db') as con:  # Заполнение таблицы с ответами на тестовую часть.
            cur = con.cursor()
            control_test_data = cur.execute("""select * from controltest""").fetchall()
            for i, row in enumerate(control_test_data):
                for j, elem in enumerate(row):
                    self.test_table.setItem(i, j, QTableWidgetItem(str(elem)))
            con.commit()  # ↓ Заполнение таблицы с ответами на письменную часть.
        with sqlite3.connect('доп файлы/control answers.db') as con:
            cur = con.cursor()
            control_writing_data = cur.execute("""select * from controlwriting""").fetchall()
            for i, row in enumerate(control_writing_data):
                for j, elem in enumerate(row):
                    self.writing_table.setItem(i, j, QTableWidgetItem(elem))
            con.commit()
        self.exit_btn.clicked.connect(self.close_window)

    def close_window(self):
        stacked_windows.resize(560, 300)
        open_window(8)
        stacked_windows.removeWidget(self)
