import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QPainter, QPixmap, QColor
from window import Ui_Dialog
import sqlite3
from random import randint


class MyWidget(QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_yes.clicked.connect(self.yes)
        self.btn_no.clicked.connect(self.no)
        self.id = 0
        self.money = 50
        self.army = 50
        self.beh = 50
        self.eco = 50
        self.days = 0
        self.lose = False
        self.fill_window()

    def paintEvent(self, e):
        self.paint = QPainter()
        self.paint.begin(self)
        lst = [self.eco, self.beh, self.army, self.money]
        for i in range(4):
            self.paint.setBrush(QColor(255, 255, 255))
            self.paint.drawRect(200 + 20 * i, 10, 10, 50)
            self.paint.setBrush(QColor(0, 0, 0))
            self.paint.drawRect(200 + 20 * i, 60 - lst[i] // 2, 10, lst[i] // 2)
        self.paint.end()

    def fill_window(self, a=randint(1, 9)):
        with sqlite3.connect('questions_bd.sqlite') as con:
            cur = con.cursor()
            while a == self.id:
                a = randint(1, 9)
            self.id = a
            result = cur.execute(f"""SELECT picture, question
                                     FROM questions where id = {a}""").fetchall()
            px3 = QPixmap(f'ends/{result[0][0]}')
            self.question.setText(result[0][1])
            self.image.setPixmap(px3)

    def yes(self):
        if not self.lose:
            with sqlite3.connect('questions_bd.sqlite') as con:
                cur = con.cursor()
                result = cur.execute(f"""SELECT eco_index1, beh_index1, army_index1, money_index1 
                                         FROM questions where id = {self.id}""").fetchall()
                a, b, c, d = [int(i) for i in result[0]]
                self.repaint()
                self.eco += a
                self.beh += b
                self.army += c
                self.money += d
                self.update()
                self.fill_window()
                self.losing_check()
                self.days += 1
                self.days_counter.display(self.days)

    def no(self):
        if not self.lose:
            with sqlite3.connect('questions_bd.sqlite') as con:
                cur = con.cursor()
                result = cur.execute(f"""SELECT eco_index2, beh_index2, army_index2, money_index2
                                         FROM questions where id = {self.id}""").fetchall()
                a, b, c, d = [int(i) for i in result[0]]
                self.repaint()
                self.eco += a
                self.beh += b
                self.army += c
                self.money += d
                self.update()
                self.fill_window()
                self.losing_check()
                self.days += 1
                self.days_counter.display(self.days)

    def losing_check(self):
        if 100 <= self.eco >= 0 or 100 <= self.beh >= 0 or 100 <= self.army >= 0 or 100 <= self.money >= 0:
            self.question.setText('Вы проиграли')
            self.lose = True


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())




