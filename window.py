from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(360, 640)

        self.btn_no = QtWidgets.QPushButton(Dialog)
        self.btn_no.setGeometry(QtCore.QRect(20, 595, 80, 25))
        self.btn_no.setObjectName("btn_no")

        self.btn_yes = QtWidgets.QPushButton(Dialog)
        self.btn_yes.setGeometry(QtCore.QRect(260, 595, 80, 25))
        self.btn_yes.setObjectName("btn_yes")

        self.days_counter = QtWidgets.QLCDNumber(Dialog)
        self.days_counter.setGeometry(QtCore.QRect(10, 10, 160, 70))
        self.days_counter.setObjectName("lcdNumber")

        self.image = QtWidgets.QLabel(Dialog)
        self.image.setGeometry(QtCore.QRect(30, 145, 320, 300))
        self.image.setText("")
        self.image.setObjectName("label")

        self.question = QtWidgets.QLabel(Dialog)
        self.question.setGeometry(QtCore.QRect(30, 495, 300, 90))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.question.setFont(font)
        self.question.setText("")
        self.question.setObjectName("label_2")
        self.question.setWordWrap(True)

        self.name = QtWidgets.QLabel(Dialog)
        self.name.setGeometry(QtCore.QRect(30, 455, 300, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.name.setFont(font)
        self.name.setText("")
        self.name.setAlignment(Qt.AlignCenter)
        self.name.setObjectName("label_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btn_yes.setText(_translate("Dialog", "Согласиться"))
        self.btn_no.setText(_translate("Dialog", "Отказаться"))
