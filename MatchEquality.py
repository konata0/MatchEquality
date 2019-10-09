import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import numpy as np
import json


class MainWindow(object):
    def __init__(self):
        self.centralWidget = None
        self.main_window = None
        # 组件
        self.button_open = None
        self.label_message = None
        self.label_question = None
        self.label_question_img = []
        self.label_answer = None
        self.label_answer_img = []
        # 变量
        self.move_number = 1
        self.if_equality = False
        # 读取火柴移动规则
        file = open('./data/rule.json', encoding='utf-8')
        self.rule = json.loads(file.read())
        file.close()
        # 读取题库
        file = open('./data/question.json', encoding='utf-8')
        self.question = json.loads(file.read())
        file.close()

    def setup_ui(self, main_window):
        self.main_window = main_window
        self.main_window.setObjectName("mainWindow")
        self.main_window.setWindowModality(QtCore.Qt.WindowModal)
        self.main_window.setFixedSize(1280, 720)
        self.main_window.setStyleSheet("#mainWindow{background-color: #f6f6f6}")

        self.centralWidget = QtWidgets.QWidget(self.main_window)
        self.centralWidget.setObjectName("centralWidget")

        # 按钮
        # 打开
        self.button_open = QtWidgets.QPushButton(self.centralWidget)
        self.button_open.setGeometry(QtCore.QRect(1100, 20, 120, 40))
        self.button_open.setObjectName("button_open")
        self.button_open.setText("打开")
        #self.button_open.clicked.connect(self.reload)

        # LABEL
        # 提示信息
        self.label_message = QtWidgets.QLabel(self.centralWidget)
        self.label_message.setGeometry(QtCore.QRect(20, 10, 800, 30))
        self.label_message.setObjectName("label_message")
        self.label_message.setWordWrap(True)
        self.set_label_message()
        # 题目
        self.label_question = QtWidgets.QLabel(self.centralWidget)
        self.label_question.setGeometry(QtCore.QRect(20, 40, 800, 30))
        self.label_question.setObjectName("label_question")
        self.label_question.setText("题目：")
        self.label_question_img = [None, None, None, None, None, None, None, None]
        for i in range(0, 8):
            self.label_question_img[i] = QtWidgets.QLabel(self.centralWidget)
            self.label_question_img[i].setGeometry(QtCore.QRect(20 + i * 120, 70, 120, 200))
            self.label_question_img[i].setObjectName("label_question_img" + str(i))
            self.label_question_img[i].setText("")
            self.label_question_img[i].setStyleSheet("QLabel{background:white;}")
        # 解答
        self.label_answer = QtWidgets.QLabel(self.centralWidget)
        self.label_answer.setGeometry(QtCore.QRect(20, 270, 800, 30))
        self.label_answer.setObjectName("label_answer")
        self.label_answer.setText("解答：")
        self.label_answer_img = [None, None, None, None, None, None, None, None]
        for i in range(0, 8):
            self.label_answer_img[i] = QtWidgets.QLabel(self.centralWidget)
            self.label_answer_img[i].setGeometry(QtCore.QRect(20 + i * 120, 300, 120, 200))
            self.label_answer_img[i].setObjectName("label_answer_img" + str(i))
            self.label_answer_img[i].setText("")
            self.label_answer_img[i].setStyleSheet("QLabel{background:white;}")






        self.main_window.setCentralWidget(self.centralWidget)
        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.main_window.setWindowTitle(_translate("mainWindow", "移动火柴"))

    def set_label_message(self):
        string = "当前设置：     移动火柴数量："
        string += str(self.move_number) + "根     等式/非等式："
        if self.if_equality:
            string += "等式"
        else:
            string += "非等式"
        self.label_message.setText(string)

    def get_move_results(self, origin, operation):
        return self.rule[origin][operation]


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setup_ui(window)
    window.show()
    sys.exit(app.exec_())















