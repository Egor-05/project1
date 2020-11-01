from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(360, 600)

        self.btn_yes = QtWidgets.QPushButton(Dialog)
        self.btn_yes.setGeometry(QtCore.QRect(20, 555, 80, 25))
        self.btn_yes.setObjectName("pushButton")

        self.btn_no = QtWidgets.QPushButton(Dialog)
        self.btn_no.setGeometry(QtCore.QRect(270, 555, 80, 25))
        self.btn_no.setObjectName("pushButton_2")

        self.days_counter = QtWidgets.QLCDNumber(Dialog)
        self.days_counter.setGeometry(QtCore.QRect(10, 10, 160, 100))
        self.days_counter.setObjectName("lcdNumber")

        self.image = QtWidgets.QLabel(Dialog)
        self.image.setGeometry(QtCore.QRect(30, 130, 320, 300))
        self.image.setText("")
        self.image.setObjectName("label")

        self.question = QtWidgets.QLabel(Dialog)
        self.question.setGeometry(QtCore.QRect(30, 460, 300, 70))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.question.setFont(font)
        self.question.setText("")
        self.question.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
