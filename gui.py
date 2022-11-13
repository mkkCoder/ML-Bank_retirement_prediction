import numpy as np
from gui_model_function import predict_y
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QTextEdit, QLineEdit
from PyQt5.QtGui import QDoubleValidator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.inputsArray = []

        # CENTER LAYOUT
        centerLayout = QVBoxLayout()
        self.setLayout(centerLayout)

        # WINDOW SETTINGS
        self.setWindowTitle("AI Program")
        # self.setFixedSize(QSize(350,800))

        # LAYOUTS
        HLayout = QHBoxLayout()
        HLayout.setAlignment(Qt.AlignHCenter)
        col1 = QVBoxLayout()
        col1.setAlignment(Qt.AlignTop)
        col2 = QVBoxLayout()
        col2.setAlignment(Qt.AlignTop)

        # TITLE
        title = QLabel("Bank - Retirment Prediction")
        font = title.font()
        font.setPointSize(30)
        font.setBold(True)
        title.setFont(font)
        title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        centerLayout.addWidget(title)

        # LABELS AND TEXT EDITS
        label1 = QLabel("Age:")
        self.edittext1 = QLineEdit()
        self.edittext1.setValidator(QDoubleValidator())
        self.edittext1.setFixedSize(QSize(150, 25))
        self.inputsArray.append(self.edittext1)
        col1.addWidget(label1)
        col1.addWidget(self.edittext1)

        label2 = QLabel("Savings:")
        self.edittext2 = QLineEdit()
        self.edittext2.setValidator(QDoubleValidator())
        self.edittext2.setFixedSize(QSize(150, 25))
        self.inputsArray.append(self.edittext2)
        col1.addWidget(label2)
        col1.addWidget(self.edittext2)

        self.answerButton = QPushButton("Get Answer")
        self.answerButton.clicked.connect(self.getAnswerFunc)
        self.answerButton.setFixedHeight(50)
        self.answerButton.setFixedHeight(50)

        self.answer = QLineEdit("ANSWER".upper())
        self.answer.setFixedHeight(40)
        self.answer.setAlignment(Qt.AlignCenter)
        self.answer.setDisabled(True)
    
        centerLayout.addLayout(HLayout)
        HLayout.addLayout(col1)
        HLayout.addLayout(col2)
        centerLayout.addWidget(self.answerButton)
        centerLayout.addWidget(self.answer)
        #making the answer more visible
        self.answer.setStyleSheet("color: white; background-color: black;")




        widget = QWidget()
        widget.setLayout(centerLayout)
        self.setCentralWidget(widget)

    def getAnswerFunc(self):
        allInputsFull = True
        inputsValues = []

        for input in self.inputsArray:
            if input.text() == "":
                allInputsFull = False
                break
            inputsValues.append(input.text())

        if allInputsFull == True:
            vals = np.array(inputsValues)
            vals = np.expand_dims(vals, axis=0)

            pred = predict_y(vals)
            if pred == 1:
                self.answer.setText('You can retire')
            else:
                self.answer.setText('You cannot retire')

app = QApplication([])

window = MainWindow()
window.show()

app.exec()