import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QPainter, QPixmap
from window import Ui_Dialog
import csv


class MyWidget(QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.btn_yes.clicked.connect()
        # self.btn_no.clicked.connect()
        self.money = 50
        self.army = 50
        self.beh = 50
        self.eco = 50
        px1 = QPixmap('image.jpg')
        px2 = QPixmap('voenp.jpg')
        self.image.setPixmap(px1)
        self.question.setPixmap(px2)

    def paintEvent(self, e):
        self.paint = QPainter()
        self.paint.begin(self)
        self.paint.drawRect(300, 10, 10, 100)
        self.paint.end()

    # def yes(self):
    #
    # def no(self):


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())




