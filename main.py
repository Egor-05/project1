import sys
from PyQt5 import QtWidgets
from PyQt5.Qt import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QPixmap, QColor
from PyQt5.QtCore import QRect
from window import Ui_Dialog
import sqlite3
from random import randint


class MyWidget(QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_yes.clicked.connect(self.yes)
        self.btn_no.clicked.connect(self.no)
        self.lst = [0, 0, 0, 0]
        self.id = 0
        self.money = 50
        self.army = 50
        self.beh = 50
        self.eco = 50
        self.days = 0
        self.lose = False
        self.fill_window()
        self.setMouseTracking(True)
        qApp.installEventFilter(self)

    def paintEvent(self, e):
        paint = QPainter()
        paint.begin(self)
        lst = [self.eco, self.beh, self.army, self.money]
        for i in range(4):
            paint.setBrush(QColor(255, 255, 255))
            paint.drawRect(200 + 20 * i, 30, 10, 50)
            paint.setBrush(QColor(0, 0, 0))
            paint.drawRect(200 + 20 * i, 80 - lst[i] // 2, 10, lst[i] // 2)
        for i in range(4):
            paint.setBrush(QColor(0, 0, 0))
            paint.drawEllipse(200 + 20 * i + (3 if self.lst[i] == 10 else 0),
                              10 + (3 if self.lst[i] == 10 else 0),
                              self.lst[i] // 2, self.lst[i] // 2)
        paint.end()

    def fill_window(self, a=randint(1, 9)):
        with sqlite3.connect('questions_bd.sqlite') as con:
            cur = con.cursor()
            while a == self.id:
                a = randint(1, 9)
            self.id = a
            result = cur.execute(f"""SELECT picture, question, person
                                     FROM questions where id = {a}""").fetchall()
            px3 = QPixmap('image.png')
            # px3 = QPixmap(result[0][0])
            self.question.setText(result[0][1])
            self.name.setText(result[0][2])
            self.image.setPixmap(px3)

    def eventFilter(self, obj, event):
        if obj.objectName() == 'btn_no':
            if event.type() == QEvent.Enter:
                with sqlite3.connect('questions_bd.sqlite') as con:
                    cur = con.cursor()
                    result = cur.execute(f"""SELECT eco_index2, beh_index2, army_index2, money_index2
                                             FROM questions where id = {self.id}""").fetchall()
                    self.lst = [abs(int(i)) for i in result[0]]
                    self.repaint()
                    self.update()
            if event.type() == QEvent.Leave:
                self.lst = [0, 0, 0, 0]
                self.repaint()
                self.update()
        if obj.objectName() == 'btn_yes':
            if event.type() == QEvent.Enter:
                with sqlite3.connect('questions_bd.sqlite') as con:
                    cur = con.cursor()
                    result = cur.execute(f"""SELECT eco_index1, beh_index1, army_index1, money_index1 
                                                 FROM questions where id = {self.id}""").fetchall()
                    self.lst = [abs(int(i)) for i in result[0]]
                    self.repaint()
                    self.update()
            if event.type() == QEvent.Leave:
                self.lst = [0, 0, 0, 0]
                self.repaint()
                self.update()
        return QWidget.eventFilter(self, obj, event)

    def yes(self):
        if not self.lose:
            with sqlite3.connect('questions_bd.sqlite') as con:
                self.repaint()
                cur = con.cursor()
                result = cur.execute(f"""SELECT eco_index1, beh_index1, army_index1, money_index1 
                                         FROM questions where id = {self.id}""").fetchall()
                a, b, c, d = [int(i) for i in result[0]]
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
                self.repaint()
                cur = con.cursor()
                result = cur.execute(f"""SELECT eco_index2, beh_index2, army_index2, money_index2
                                         FROM questions where id = {self.id}""").fetchall()
                a, b, c, d = [int(i) for i in result[0]]
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
        if 100 <= self.eco:
            self.question.setText('Вы проиграли')
            px = QPixmap('ends/deport.png')
            self.image.setPixmap(px)
            self.lose = True
        elif self.eco <= 0:
            self.question.setText('Вы проиграли')
            px = QPixmap('ends/rad.png')
            self.image.setPixmap(px)
            self.lose = True
        elif 100 <= self.beh:
            self.question.setText('Вы проиграли')
            px = QPixmap('ends/dead.jpg')
            self.image.setPixmap(px)
            self.lose = True
        elif self.beh <= 0:
            self.question.setText('Вы проиграли')
            px = QPixmap('ends/vis.jpg')
            self.image.setPixmap(px)
            self.lose = True
        elif 100 <= self.army:
            self.question.setText('Вы проиграли')
            px = QPixmap('ends/vp.png')
            self.image.setPixmap(px)
            self.lose = True
        elif self.army <= 0:
            self.question.setText('Вы проиграли')
            px = QPixmap('ends/zasada.jpg')
            self.image.setPixmap(px)
            self.lose = True
        elif 100 <= self.money:
            self.question.setText('Вы проиграли')
            px = QPixmap('ends/bank.png')
            self.image.setPixmap(px)
            self.lose = True
        # elif self.money <= 0:
        #     self.question.setText('Вы проиграли')
        #     px = QPixmap('ends/')
        #     self.image.setPixmap(px)
        #     self.lose = True
        if self.lose:
            self.name.setText('')


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())





