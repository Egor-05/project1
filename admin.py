from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QApplication, QPushButton, QTableWidget, QMessageBox
import sqlite3
import sys


class Example(QWidget):
    id = -1

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Административный интерфейс')
        self.setGeometry(629, 357, 629, 357)

        self.pushButton = QPushButton(self)
        self.pushButton.move(10, 10)
        self.pushButton.resize(611, 25)
        self.pushButton.setObjectName("pushButton_2")
        self.pushButton.clicked.connect(self.save_changes)
        self.pushButton.setText("Сохранить")

        self.tableWidget = QTableWidget(self)
        self.tableWidget.move(10, 50)
        self.tableWidget.resize(611, 301)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.con = sqlite3.connect("questions_bd.sqlite")
        self.fill_table()

    def fill_table(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM questions").fetchall()
        self.titles = [description[0] for description in cur.description]
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(self.titles) - 1)
        self.tableWidget.setHorizontalHeaderLabels(self.titles[1:])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem[1:]):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Insert:
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setCurrentCell(rowPosition, 0)
        elif e.key() == Qt.Key_Delete:
            self.id = self.tableWidget.currentRow()
            valid = QMessageBox.question(self.tableWidget, '', 'Вы действительно хотите удалить элемент?',
                                         QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                self.save_changes()

    def save_changes(self):
        valid = QMessageBox.question(self.tableWidget, '', 'Вы действительно хотите сохранить изменения?',
                                     QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            result = cur.execute("SELECT id FROM questions").fetchall()
            length = 0
            for i in result:
                length += 1
            rows = self.tableWidget.rowCount()
            cols = self.tableWidget.columnCount()
            data = []
            s = -1
            for row in range(rows):
                s += 1
                if s == self.id:
                    continue
                tmp = []
                for col in range(cols):
                    tmp.append(self.tableWidget.item(row, col).text())
                data.append(tmp)
            for i in data:
                for j in [i[-1], i[-2], i[-3], i[-4], i[-6], i[-7], i[-8], i[-9]]:
                    try:
                        int(j)
                    except Exception:
                        valid = QMessageBox.question(self.tableWidget, '',
                                                     'Неверные значения в числовых полях',
                                                     QMessageBox.Ok)
                        return
            self.id = -1
            cur.execute("DELETE FROM questions")
            self.con.commit()
            for i in data:
                cur.execute("""INSERT INTO questions ( 
                                  question,
                                  person,
                                  picture,
                                  answer1,
                                  eco_index1,
                                  beh_index1,
                                  army_index1,
                                  money_index1,
                                  answer2,
                                  eco_index2,
                                  beh_index2,
                                  army_index2,
                                  money_index2)
                                  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", i)
            self.con.commit()
            self.fill_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())