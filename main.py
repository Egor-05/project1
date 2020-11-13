import sys
from PyQt5.Qt import *
from PyQt5.QtWidgets import QApplication, QMainWindow
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
        self.lst = [0, 0, 0, 0]
        self.id = 0
        self.money = 50
        self.army = 50
        self.beh = 50
        self.eco = 50
        self.days = 0
        px1 = QPixmap('iсons/list.png')
        px2 = QPixmap('iсons/man.png')
        px3 = QPixmap('iсons/avt.png')
        px4 = QPixmap('iсons/mon.png')
        self.ikon1.setPixmap(px1)
        self.ikon2.setPixmap(px2)
        self.ikon3.setPixmap(px3)
        self.ikon4.setPixmap(px4)
        self.lose = False
        self.fill_window()
        self.setMouseTracking(True)
        qApp.installEventFilter(self)

    # Функция отрисовки, а также введения в начале
    def paintEvent(self, e):
        paint = QPainter()
        paint.begin(self)
        lst = [self.eco, self.beh, self.army, self.money]
        for i in range(4):
            paint.setBrush(QColor(255, 255, 255))
            paint.drawRect(240 + 20 * i, 25, 10, 50)
            paint.setBrush(QColor(0, 0, 0))
            paint.drawRect(240 + 20 * i, 75 - lst[i] // 2, 10, lst[i] // 2)
        for i in range(4):
            paint.setBrush(QColor(0, 0, 0))
            paint.drawEllipse(240 + 20 * i + (3 if self.lst[i] == 10 else 0),
                              5 + (3 if self.lst[i] == 10 else 0),
                              self.lst[i] // 2, self.lst[i] // 2)
        paint.end()

    # функция замены имени, фото, вопроса, текста на кнопках
    def fill_window(self, a=randint(1, 9)):
        if self.days == self.id == 0:
            valid = QMessageBox.question(self.days_counter, 'Введение', 'Итак начинаем, но сначала прочитайте основное '
                                                                        'правило: у вас есть 4 шкалы, каждая '
                                                                        'отвечает за свой вид ресурса, нельзя допустить'
                                                                        ' что бы какая либо из шкал заполнилась или '
                                                                        'опустела, на сколько изменится шкала будут '
                                                                        'показывать круги над ними, игра бесконечна. '
                                                                        'Удачи!',
                                         QMessageBox.Ok)
        with sqlite3.connect('questions_bd.sqlite') as con:
            cur = con.cursor()
            while a == self.id:
                a = randint(1, 20)
            self.id = a
            result = cur.execute(f"""SELECT picture, question, person, answer1, answer2
                                     FROM questions where id = {a}""").fetchall()
            px3 = QPixmap(result[0][0])
            self.question.setText(result[0][1])
            self.name.setText(result[0][2])
            self.image.setPixmap(px3)
            self.btn_yes.setText(result[0][3])
            self.btn_no.setText(result[0][4])

    # Функция для проверки наведен ли курсор на кнопки
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

    #функция для обрабаотки согласия
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

    # Функция для кнопки отказа
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

    # обработка проигрыша
    def losing_check(self):
        if 100 <= self.eco:
            self.question.setText('Экология была нормализована, '
                                  'но вас обвиниле в попытке помешать этому и выслали из страны')
            px = QPixmap('ends/deport.png')
            self.image.setPixmap(px)
            self.lose = True
        elif self.eco <= 0:
            self.question.setText('На Земле появился новый вирус, который начал убивать население. '
                                  'Вы умираете одним из первых')
            px = QPixmap('ends/rad.png')
            self.image.setPixmap(px)
            self.lose = True
        elif 100 <= self.beh:
            self.question.setText('Вы умерли от инфарка, но вас признали лучшим правителем страны')
            px = QPixmap('ends/dead.jpg')
            self.image.setPixmap(px)
            self.lose = True
        elif self.beh <= 0:
            self.question.setText('Народ поднял восстание, и вас повесили на клавной площади')
            px = QPixmap('ends/vis.jpg')
            self.image.setPixmap(px)
            self.lose = True
        elif 100 <= self.army:
            self.question.setText('Военные устроили переворот и вы были отправлены в ссылку')
            px = QPixmap('ends/vp.png')
            self.image.setPixmap(px)
            self.lose = True
        elif self.army <= 0:
            self.question.setText('Началась война и вы пытаясь добраться до штаба умерли попав в засаду')
            px = QPixmap('ends/zasada.jpg')
            self.image.setPixmap(px)
            self.lose = True
        elif 100 <= self.money:
            self.question.setText('Банки захватили власть')
            px = QPixmap('ends/bank.png')
            self.image.setPixmap(px)
            self.lose = True
        elif self.money <= 0:
            self.question.setText('ВСтрана увязла в долгах и вашу голову обменяли на их списание')
            px = QPixmap('ends/head.png')
            self.image.setPixmap(px)
            self.lose = True
        if self.lose:
            self.name.setText('')
            valid = QMessageBox.question(self.days_counter, '', f"Поздравляем, вы продержались "
                                         f"{int(self.days_counter.value())} дней", QMessageBox.Ok)


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())





