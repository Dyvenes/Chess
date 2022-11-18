from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QButtonGroup
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
        self.close()


class Choise_color(QWidget, Ui_Form):
    color = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        print("choise color")
        self.buttonGroup.buttonClicked.connect(self.send_signal)

    def send_signal(self, btn):
        print("closed")
        self.color.emit(btn.text())
        self.close()


class end_of_game(QWidget, Ui_Form_2):
    choise = pyqtSignal(str)

    def __init__(self, color):
        super().__init__()
        self.color = color
        if self.color:
            self.label.setText('БЕЛЫЕ ВЫИГРАЛИ!')
        else:
            self.label.setText('ЧЕРНЫЕ ВЫИГРАЛИ!')
        self.buttonGroup.buttonClicked.connect(self.send_signal)

    def send_signal(self, btn):
        self.choise.emit(btn.text())
        self.close()