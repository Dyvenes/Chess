import sqlite3

from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QButtonGroup, QTableWidget, \
    QTableWidgetItem, QDialog
from PyQt5.QtCore import pyqtSignal
from choise_color import Ui_Form
from victory import Ui_Form_2
from choise_figure import Ui_Choise_dialog


class Choise_figure(QDialog, Ui_Choise_dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.figure = None
        self.buttonGroup.buttonClicked.connect(self.send_signal)

    def send_signal(self, btn):
        self.figure = btn.text()
        self.accept()


class Choise_color(QWidget, Ui_Form):
    color = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('НАЧАЛО ИГРЫ')
        self.buttonGroup.buttonClicked.connect(self.send_signal)

    def send_signal(self, btn):
        lineEdit_txt = self.lineEdit.text()
        if lineEdit_txt:
            self.color.emit(btn.text() + lineEdit_txt)
            self.close()
        else:
            pass


class End_of_game(QWidget, Ui_Form_2):
    choise = pyqtSignal(str)

    def __init__(self, color):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('ПОБЕДА')
        self.color = color
        if self.color:
            self.label.setText('БЕЛЫЕ ВЫИГРАЛИ!')
        else:
            self.label.setText('ЧЕРНЫЕ ВЫИГРАЛИ!')
        self.buttonGroup.buttonClicked.connect(self.send_signal)

    def send_signal(self, btn):
        self.choise.emit(btn.text())
        self.close()


class Statistic_rend(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('СТАТИСТИКА ИГРОКОВ')
        self.verLayout = QVBoxLayout(self)
        self.setGeometry(300, 300, 900, 300)
        self.tableWidget = QTableWidget(self)
        self.layout().addWidget(self.tableWidget)
        self.update_result()

    def update_result(self):
        con = sqlite3.connect("chess_db.db")
        cur = con.cursor()
        result = cur.execute(
            'SELECT nicks, "колличество игр", "колличество побед", "% побед", '
            '"максимальное колличесвто шагов", "минимальное колличество шагов" FROM statistic').fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Никто не играл(')
            return
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i in range(len(self.titles)):
            self.tableWidget.setItem(0, i, QTableWidgetItem(self.titles[i]))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}
