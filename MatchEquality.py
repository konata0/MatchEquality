import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import numpy as np
import json
import cv2


def question_string_normal_to_standard(question_string):
    string_list = question_string.split("=", 1)
    number3 = string_list[1]
    operation = "+"
    if "-" in string_list[0]:
        operation = "-"
    if "*" in string_list[0]:
        operation = "*"
    string_list = string_list[0].split(operation, 1)
    number1 = string_list[0]
    number2 = string_list[1]
    re = ""
    if len(number1) == 1:
        re += "?"
    re += number1
    re += operation
    if len(number2) == 1:
        re += "?"
    re += number2
    re += "="
    if len(number3) == 1:
        re += "?"
    re += number3
    return re


def question_string_standard_to_normal(question_string):
    return question_string.replace('?', '')


class MainWindow(object):
    def __init__(self):
        self.centralWidget = None
        self.main_window = None
        # 组件
        self.label_message = None
        self.label_question = None
        self.label_question_img = []
        self.label_answer = None
        self.label_answer_img = []
        self.label_setting = None
        self.button_move_1 = None
        self.button_move_2 = None
        self.button_equality = None
        self.button_not_equality = None
        self.question_list = None
        self.question_list_string = None
        # 变量
        self.move_number = 1
        self.if_equality = False
        # 读取火柴移动规则
        file = open('./data/rule.json', encoding='utf-8')
        self.rule = json.loads(file.read())
        file.close()
        # 读取题库
        file = open('./data/question.json', encoding='utf-8')
        self.questions = json.loads(file.read())
        file.close()
        self.question = self.questions[0]["question"]
        self.move_number = self.questions[0]["moveNumber"]
        self.if_equality = self.questions[0]["equality"]

    def setup_ui(self, main_window):
        self.main_window = main_window
        self.main_window.setObjectName("mainWindow")
        self.main_window.setWindowModality(QtCore.Qt.WindowModal)
        self.main_window.setFixedSize(1280, 720)
        self.main_window.setStyleSheet("#mainWindow{background-color: #f6f6f6}")

        self.centralWidget = QtWidgets.QWidget(self.main_window)
        self.centralWidget.setObjectName("centralWidget")

        # 按钮
        # 选择题库
        self.button_move_1 = QtWidgets.QPushButton(self.centralWidget)
        self.button_move_1.setGeometry(QtCore.QRect(1000, 580, 120, 40))
        self.button_move_1.setObjectName("button_move_1")
        self.button_move_1.setText("移动1根火柴")
        self.button_move_1.clicked.connect(self.button_move_1_click)
        self.button_move_2 = QtWidgets.QPushButton(self.centralWidget)
        self.button_move_2.setGeometry(QtCore.QRect(1140, 580, 120, 40))
        self.button_move_2.setObjectName("button_move_2")
        self.button_move_2.setText("移动2根火柴")
        self.button_move_2.clicked.connect(self.button_move_2_click)
        self.button_not_equality = QtWidgets.QPushButton(self.centralWidget)
        self.button_not_equality.setGeometry(QtCore.QRect(1000, 640, 120, 40))
        self.button_not_equality.setObjectName("button_not_equality")
        self.button_not_equality.setText("非等式")
        self.button_not_equality.clicked.connect(self.button_not_equality_click)
        self.button_equality = QtWidgets.QPushButton(self.centralWidget)
        self.button_equality.setGeometry(QtCore.QRect(1140, 640, 120, 40))
        self.button_equality.setObjectName("button_equality")
        self.button_equality.setText("等式")
        self.button_equality.clicked.connect(self.button_equality_click)

        # LABEL
        # 提示信息
        self.label_message = QtWidgets.QLabel(self.centralWidget)
        self.label_message.setGeometry(QtCore.QRect(1000, 10, 260, 60))
        self.label_message.setObjectName("label_message")
        self.label_message.setWordWrap(True)
        self.set_label_message()
        # 题目
        self.label_question = QtWidgets.QLabel(self.centralWidget)
        self.label_question.setGeometry(QtCore.QRect(20, 10, 800, 30))
        self.label_question.setObjectName("label_question")
        self.label_question.setText("题目：")
        self.label_question_img = [None, None, None, None, None, None, None, None]
        for i in range(0, 8):
            self.label_question_img[i] = QtWidgets.QLabel(self.centralWidget)
            self.label_question_img[i].setGeometry(QtCore.QRect(20 + i * 120, 50, 120, 200))
            self.label_question_img[i].setObjectName("label_question_img" + str(i))
            self.label_question_img[i].setText("")
            self.label_question_img[i].setStyleSheet("QLabel{background:white;}")
        self.set_question_img(self.question)
        # 解答
        self.label_answer = QtWidgets.QLabel(self.centralWidget)
        self.label_answer.setGeometry(QtCore.QRect(20, 260, 800, 30))
        self.label_answer.setObjectName("label_answer")
        self.label_answer.setText("解答：")
        self.label_answer_img = [None, None, None, None, None, None, None, None]
        for i in range(0, 8):
            self.label_answer_img[i] = QtWidgets.QLabel(self.centralWidget)
            self.label_answer_img[i].setGeometry(QtCore.QRect(20 + i * 120, 300, 120, 200))
            self.label_answer_img[i].setObjectName("label_answer_img" + str(i))
            self.label_answer_img[i].setText("")
            self.label_answer_img[i].setStyleSheet("QLabel{background:white;}")
        # 提示信息
        self.label_setting = QtWidgets.QLabel(self.centralWidget)
        self.label_setting.setGeometry(QtCore.QRect(1000, 540, 800, 30))
        self.label_setting.setObjectName("label_setting")
        self.label_setting.setText("选择题库：")

        # 题库
        self.question_list = QtWidgets.QListView(self.centralWidget)
        self.question_list.setGeometry(QtCore.QRect(1000, 80, 260, 450))
        self.question_list.setObjectName("question_list")
        self.set_question_list()

        self.main_window.setCentralWidget(self.centralWidget)
        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.main_window.setWindowTitle(_translate("mainWindow", "移动火柴"))

    def set_label_message(self):
        string = "当前题库：\n移动火柴数量："
        string += str(self.move_number) + "根\n等式/非等式："
        if self.if_equality:
            string += "等式"
        else:
            string += "非等式"
        self.label_message.setText(string)

    def set_question_img(self, question_string):
        for i in range(0, 8):
            char = question_string[i]
            if char == "?":
                char = "space"
            if char == "*":
                char = "x"
            img_path = "./data/img/" + char + ".png"
            img = QtGui.QPixmap(img_path).scaled(
                self.label_question_img[i].width(),
                self.label_question_img[i].height()
            )
            self.label_question_img[i].setPixmap(img)

    def set_answer_img(self, answer_string):
        for i in range(0, 8):
            char = answer_string[i]
            if char == "?":
                char = "space"
            if char == "*":
                char = "x"
            img_path = "./data/img/" + char + ".png"
            img = QtGui.QPixmap(img_path).scaled(
                self.label_answer_img[i].width(),
                self.label_answer_img[i].height()
            )
            self.label_answer_img[i].setPixmap(img)

    def set_question_list(self):
        self.question_list_string = [question["question"]
                                     for question in self.questions
                                     if question["moveNumber"] == self.move_number
                                     and question["equality"] == self.if_equality]
        self.question_list_string = list(map(question_string_standard_to_normal, self.question_list_string))
        slm = QtCore.QStringListModel()
        slm.setStringList(self.question_list_string)
        self.question_list.setModel(slm)
        self.question_list.clicked.connect(self.question_list_click)
        self.question_list.doubleClicked.connect(self.question_list_click)

    def question_list_click(self, index):
        self.question = question_string_normal_to_standard(self.question_list_string[index.row()])
        self.set_question_img(self.question)


    def button_move_1_click(self):
        self.move_number = 1
        self.set_label_message()
        self.set_question_list()

    def button_move_2_click(self):
        self.move_number = 2
        self.set_label_message()
        self.set_question_list()

    def button_not_equality_click(self):
        self.if_equality = False
        self.set_label_message()
        self.set_question_list()

    def button_equality_click(self):
        self.if_equality = True
        self.set_label_message()
        self.set_question_list()

    def get_move_results(self, origin, operation):
        return self.rule[origin][operation]


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setup_ui(window)
    window.show()
    sys.exit(app.exec_())















