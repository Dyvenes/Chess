import sqlite3

from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QButtonGroup, QTableWidget, \
    QTableWidgetItem
from PyQt5.QtCore import pyqtSignal
from choise_color import Ui_Form
from victory import Ui_Form_2


class Choise_figure(QWidget):
    figure = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('ВЫБОР ФИГУРЫ')
        self.verticalLayout = QVBoxLayout(self)
        self.HorLayout = QHBoxLayout(self)
        self.label = QLabel(self)
        self.label.setText('выберите фигуру, которой станет пешка:')
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QHBoxLayout(self)
        self.pushButton_4 = QPushButton(self)
        self.pushButton_4.setText('Queen')
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.pushButton_3 = QPushButton(self)
        self.pushButton_3.setText('Rook')
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setText('Knight')
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QPushButton(self)
        self.pushButton.setText('Bishop')
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.pushButton)
        self.buttonGroup.addButton(self.pushButton_2)
        self.buttonGroup.addButton(self.pushButton_3)
        self.buttonGroup.addButton(self.pushButton_4)
        self.buttonGroup.buttonClicked.connect(self.send_signal)

    def send_signal(self, btn):
        self.figure.emit(btn.text())
        print("emit")
        self.close()


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
            self.color.emit(btn.text(), lineEdit_txt)
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
        self.setGeometry(900, 300)
        self.verLayout = QVBoxLayout(self)
        self.tableWidget = QTableWidget(self)
        self.layout().addWidget(QTableWidget(self))
        self.update_result()

    def update_result(self):
        con = sqlite3.connect("chess_db.db")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM statistic").fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Никто не играл(')
            return
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

