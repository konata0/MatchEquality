import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import numpy as np
import json
import cv2


def input_check(string):
    try:
        if len(string) < 5 or len(string) > 8:
            return False
        if "=" not in string:
            return False
        string_list = string.split("=")
        if len(string_list) != 2:
            return False
        number3 = int(string_list[1])
        string = string_list[0]
        operation = "n"
        if "-" in string:
            operation = "-"
        if "*" in string:
            operation = "*"
        if "+" in string:
            operation = "+"
        if operation == "n":
            return False
        string_list = string.split(operation)
        if len(string_list) != 2:
            return False
        number1 = int(string_list[0])
        number2 = int(string_list[1])
        if number1 < 0 or number1 > 99:
            return False
        if number2 < 0 or number2 > 99:
            return False
        if number3 < 0 or number3 > 99:
            return False
    except:
        return False
    else:
        return True


def question_string_normal_to_standard(question_string):
    question_string = question_string.replace(" ", "")
    string_list = question_string.split("=", 1)
    number3 = int(string_list[1])
    operation = "+"
    if "-" in string_list[0]:
        operation = "-"
    if "*" in string_list[0]:
        operation = "*"
    string_list = string_list[0].split(operation, 1)
    number1 = int(string_list[0])
    number2 = int(string_list[1])
    re = ""
    if number1 < 10:
        re += "?"
    re += str(number1)
    re += operation
    if number2 < 10:
        re += "?"
    re += str(number2)
    re += "="
    if number3 < 10:
        re += "?"
    re += str(number3)
    return re


def question_string_standard_to_normal(question_string):
    return question_string.replace('?', '').replace(' ', '')


def equality_check(equality_string):
    if equality_string[0] == "0" or equality_string[3] == "0" or equality_string[6] == "0":
        return False
    if equality_string[1] == "?" or equality_string[4] == "?" or equality_string[7] == "?":
        return False
    equality_string = question_string_standard_to_normal(equality_string)
    string_list = equality_string.split("=")
    string = string_list[0]
    number3 = int(string_list[1])
    operation = "+"
    if "-" in string:
        operation = "-"
    if "*" in string:
        operation = "*"
    string_list = string.split(operation)
    number1 = int(string_list[0])
    number2 = int(string_list[1])
    if operation == "+":
        return number1 + number2 == number3
    if operation == "-":
        return number1 - number2 == number3
    if operation == "*":
        return number1 * number2 == number3
    return False


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
        self.button_answer = None
        self.button_add = None
        self.button_generate = None
        self.button_before = None
        self.button_next = None
        self.button_show_answer = None
        self.question_list = None
        self.question_list_string = None
        self.edit_add = None
        self.edit_answer = None
        self.edit_generate = None
        # 变量
        self.move_number = 1
        self.if_equality = False
        self.answers = None
        self.answer_index = -1
        # 读取火柴移动规则
        file = open('./data/rule.json', encoding='utf-8')
        self.rule = json.loads(file.read())
        file.close()
        file = open('./data/move.json', encoding='utf-8')
        self.move = json.loads(file.read())
        file.close()
        # 读取题库
        file = open('./data/question.json', encoding='utf-8')
        self.questions = json.loads(file.read())
        file.close()
        self.question = None
        self.move_number = self.questions[0]["moveNumber"]
        self.if_equality = self.questions[0]["equality"]

    def setup_ui(self, main_window):
        self.main_window = main_window
        self.main_window.setObjectName("mainWindow")
        self.main_window.setWindowModality(QtCore.Qt.WindowModal)
        self.main_window.setFixedSize(1280, 660)
        self.main_window.setStyleSheet("#mainWindow{background-color: #f6f6f6}")

        self.centralWidget = QtWidgets.QWidget(self.main_window)
        self.centralWidget.setObjectName("centralWidget")

        # 按钮
        # 选择题库
        self.button_move_1 = QtWidgets.QPushButton(self.centralWidget)
        self.button_move_1.setGeometry(QtCore.QRect(1000, 520, 120, 40))
        self.button_move_1.setObjectName("button_move_1")
        self.button_move_1.setText("移动1根火柴")
        self.button_move_1.clicked.connect(self.button_move_1_click)
        self.button_move_2 = QtWidgets.QPushButton(self.centralWidget)
        self.button_move_2.setGeometry(QtCore.QRect(1140, 520, 120, 40))
        self.button_move_2.setObjectName("button_move_2")
        self.button_move_2.setText("移动2根火柴")
        self.button_move_2.clicked.connect(self.button_move_2_click)
        self.button_not_equality = QtWidgets.QPushButton(self.centralWidget)
        self.button_not_equality.setGeometry(QtCore.QRect(1000, 580, 120, 40))
        self.button_not_equality.setObjectName("button_not_equality")
        self.button_not_equality.setText("非等式")
        self.button_not_equality.clicked.connect(self.button_not_equality_click)
        self.button_equality = QtWidgets.QPushButton(self.centralWidget)
        self.button_equality.setGeometry(QtCore.QRect(1140, 580, 120, 40))
        self.button_equality.setObjectName("button_equality")
        self.button_equality.setText("等式")
        self.button_equality.clicked.connect(self.button_equality_click)
        self.button_answer = QtWidgets.QPushButton(self.centralWidget)
        self.button_answer.setGeometry(QtCore.QRect(160, 520, 120, 40))
        self.button_answer.setObjectName("button_answer")
        self.button_answer.setText("作答")
        self.button_answer.clicked.connect(self.button_answer_click)
        self.button_add = QtWidgets.QPushButton(self.centralWidget)
        self.button_add.setGeometry(QtCore.QRect(160, 580, 120, 40))
        self.button_add.setObjectName("button_add")
        self.button_add.setText("添加到当前题库")
        self.button_add.clicked.connect(self.button_add_click)
        self.button_generate = QtWidgets.QPushButton(self.centralWidget)
        self.button_generate.setGeometry(QtCore.QRect(440, 520, 120, 40))
        self.button_generate.setObjectName("button_generate")
        self.button_generate.setText("由等式生成题目")
        self.button_generate.clicked.connect(self.button_generate_click)
        self.button_show_answer = QtWidgets.QPushButton(self.centralWidget)
        self.button_show_answer.setGeometry(QtCore.QRect(700, 520, 120, 40))
        self.button_show_answer.setObjectName("button_show_answer")
        self.button_show_answer.setText("显示解答")
        self.button_show_answer.clicked.connect(self.button_show_answer_click)
        self.button_before = QtWidgets.QPushButton(self.centralWidget)
        self.button_before.setGeometry(QtCore.QRect(840, 520, 120, 40))
        self.button_before.setObjectName("button_before")
        self.button_before.setText("上一解答")
        self.button_before.clicked.connect(self.button_before_click)
        self.button_next = QtWidgets.QPushButton(self.centralWidget)
        self.button_next.setGeometry(QtCore.QRect(840, 580, 120, 40))
        self.button_next.setObjectName("button_next")
        self.button_next.setText("下一解答")
        self.button_next.clicked.connect(self.button_next_click)

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
        self.label_setting.setGeometry(QtCore.QRect(1000, 490, 800, 30))
        self.label_setting.setObjectName("label_setting")
        self.label_setting.setText("选择题库：")

        # 题库
        self.question_list = QtWidgets.QListView(self.centralWidget)
        self.question_list.setGeometry(QtCore.QRect(1000, 80, 260, 400))
        self.question_list.setObjectName("question_list")
        self.set_question_list()

        # 编辑框
        # 检测回答
        self.edit_answer = QtWidgets.QLineEdit(self.centralWidget)
        self.edit_answer.setGeometry(QtCore.QRect(20, 520, 120, 40))
        self.edit_answer.setObjectName("edit_answer")
        self.edit_answer.setAlignment(QtCore.Qt.AlignCenter)
        # 添加题库
        self.edit_add = QtWidgets.QLineEdit(self.centralWidget)
        self.edit_add.setGeometry(QtCore.QRect(20, 580, 120, 40))
        self.edit_add.setObjectName("edit_add")
        self.edit_add.setAlignment(QtCore.Qt.AlignCenter)
        # 由等式生成题库
        self.edit_generate = QtWidgets.QLineEdit(self.centralWidget)
        self.edit_generate.setGeometry(QtCore.QRect(300, 520, 120, 40))
        self.edit_generate.setObjectName("edit_generate")
        self.edit_generate.setAlignment(QtCore.Qt.AlignCenter)

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
        self.question = None
        self.answers = None
        self.answer_index = -1
        self.set_question_img("????????")
        self.set_answer_img("????????")
        self.label_answer.setText("解答：")

    def question_list_click(self, index):
        self.question = question_string_normal_to_standard(self.question_list_string[index.row()])
        self.set_question_img(self.question)
        self.set_answer_img("????????")
        self.answers = None
        self.answer_index = -1
        self.label_answer.setText("解答：")

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

    def button_answer_click(self):
        string = self.edit_answer.text()
        if not input_check(string):
            QMessageBox.warning(self.main_window, "error", "输入字符串不符合格式！", QMessageBox.Ok)
            return
        string = question_string_normal_to_standard(string)
        if self.question is None:
            QMessageBox.warning(self.main_window, "error", "请先选择题目！", QMessageBox.Ok)
            return
        if self.answers is None:
            self.answers = self.get_answers(self.question, self.move_number)
        if string in self.answers:
            QMessageBox.information(self.main_window, "作答", "答案正确！", QMessageBox.Ok)
            return
        else:
            QMessageBox.information(self.main_window, "作答", "答案错误！", QMessageBox.Ok)
            return

    def button_add_click(self):
        string = self.edit_add.text()
        if not input_check(string):
            QMessageBox.warning(self.main_window, "error", "输入字符串不符合格式！", QMessageBox.Ok)
            return
        string = question_string_normal_to_standard(string)
        if self.if_equality and not equality_check(string):
            QMessageBox.warning(self.main_window, "error", "该题库要求输入等式！", QMessageBox.Ok)
            return
        if not self.if_equality and equality_check(string):
            QMessageBox.warning(self.main_window, "error", "该题库要求输入非成立等式！", QMessageBox.Ok)
            return
        answers = self.get_answers(string, self.move_number)
        if len(answers) == 0:
            QMessageBox.warning(self.main_window, "error", "该题目在当前题库条件下无解，无法添加！", QMessageBox.Ok)
            return
        exist = False
        for q in self.questions:
            if q["question"] == string and q["moveNumber"] == self.move_number and q["equality"] == self.if_equality:
                exist = True
                break
        if exist:
            QMessageBox.warning(self.main_window, "error", "该题目已经存在，无法添加！", QMessageBox.Ok)
            return
        self.questions.append({
            "question": string,
            "moveNumber": self.move_number,
            "equality": self.if_equality
        })
        with open("./data/question.json", "w") as file:
            json.dump(self.questions, file)
        QMessageBox.information(self.main_window, "添加", "添加成功，刷新题库后可见！", QMessageBox.Ok)

    def button_generate_click(self):
        answer_string = self.edit_generate.text()
        if not input_check(answer_string):
            QMessageBox.warning(self.main_window, "error", "输入字符串不符合格式！", QMessageBox.Ok)
            return
        answer_string = question_string_normal_to_standard(answer_string)
        if not equality_check(answer_string):
            QMessageBox.warning(self.main_window, "error", "要求输入等式！", QMessageBox.Ok)
            return
        re_questions = []
        move_list = self.move["move" + str(self.move_number)]
        move_allow = {
            0: ["0"],
            1: ["0"],
            2: ["0"],
            3: ["0"],
            4: ["0"],
            5: ["0"],
            6: ["0"],
            7: ["0"]
        }
        for i in [0, 1, 2, 3, 4, 6, 7]:
            element = self.rule[answer_string[i]]
            for operation in element.keys():
                if len(element[operation]) > 0:
                    move_allow[i].append(operation)
        for move in move_list:
            flag = True
            for i in range(0, 8):
                if move[i] not in move_allow[i]:
                    flag = False
                    break
            if not flag:
                continue
            move_results = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
            for i in range(0, 8):
                if move[i] == "0":
                    move_results[i].append(answer_string[i])
                else:
                    move_results[i] = self.rule[answer_string[i]][move[i]]
            for a0 in move_results[0]:
                for a1 in move_results[1]:
                    for a2 in move_results[2]:
                        for a3 in move_results[3]:
                            for a4 in move_results[4]:
                                for a5 in move_results[5]:
                                    for a6 in move_results[6]:
                                        for a7 in move_results[7]:
                                            question_string = a0 + a1 + a2 + a3 + a4 + a5 + a6 + a7
                                            if self.if_equality:
                                                if equality_check(question_string):
                                                    re_questions.append(question_string)
                                            else:
                                                if not equality_check(question_string):
                                                    re_questions.append(question_string)
        if len(re_questions) == 0:
            QMessageBox.warning(self.main_window, "error", "该等式无法生成满足该题库条件的题目！", QMessageBox.Ok)
            return
        msg = "生成题目有：\n"
        t = 0
        for q in re_questions:
            t += 1
            msg += question_string_standard_to_normal(q) + "    "
            if t == 3:
                t = 0
                msg += "\n"
        msg += "\n\n是否添加题目到题库？"
        re = QMessageBox.information(self.main_window, "生成题目", msg, QMessageBox.Yes | QMessageBox.No)
        if re == QMessageBox.Yes:
            for q in re_questions:
                exist = False
                for exist_q in self.questions:
                    if exist_q["question"] == q and exist_q["moveNumber"] == self.move_number and exist_q["equality"] == self.if_equality:
                        exist = True
                        break
                if not exist:
                    self.questions.append({
                        "question": q,
                        "moveNumber": self.move_number,
                        "equality": self.if_equality
                    })
                    with open("./data/question.json", "w") as file:
                        json.dump(self.questions, file)
            QMessageBox.information(self.main_window, "添加", "添加成功，刷新题库后可见！", QMessageBox.Ok)

    def button_show_answer_click(self):
        if self.question is None:
            QMessageBox.warning(self.main_window, "error", "请先选择题目！", QMessageBox.Ok)
            return
        if self.answers is None:
            self.answers = self.get_answers(self.question, self.move_number)
        self.answer_index = 0
        self.label_answer.setText("解答（" + str(self.answer_index + 1) + "/" + str(len(self.answers)) + "）：")
        self.set_answer_img(self.answers[self.answer_index])

    def button_before_click(self):
        if self.answers is None:
            QMessageBox.warning(self.main_window, "error", "请先显示解答！", QMessageBox.Ok)
            return
        if self.answer_index == 0:
            self.answer_index = len(self.answers) - 1
        else:
            self.answer_index -= 1
        self.label_answer.setText("解答（" + str(self.answer_index + 1) + "/" + str(len(self.answers)) + "）：")
        self.set_answer_img(self.answers[self.answer_index])

    def button_next_click(self):
        if self.answers is None:
            QMessageBox.warning(self.main_window, "error", "请先显示解答！", QMessageBox.Ok)
            return
        if self.answer_index == len(self.answers) - 1:
            self.answer_index = 0
        else:
            self.answer_index += 1
        self.label_answer.setText("解答（" + str(self.answer_index + 1) + "/" + str(len(self.answers)) + "）：")
        self.set_answer_img(self.answers[self.answer_index])

    def get_answers(self, question_string, move_number):
        re_answers = []
        move_list = self.move["move" + str(move_number)]
        move_allow = {
            0: ["0"],
            1: ["0"],
            2: ["0"],
            3: ["0"],
            4: ["0"],
            5: ["0"],
            6: ["0"],
            7: ["0"]
        }
        for i in [0, 1, 2, 3, 4, 6, 7]:
            element = self.rule[question_string[i]]
            for operation in element.keys():
                if len(element[operation]) > 0:
                    move_allow[i].append(operation)
        for move in move_list:
            flag = True
            for i in range(0, 8):
                if move[i] not in move_allow[i]:
                    flag = False
                    break
            if not flag:
                continue
            move_results = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
            for i in range(0, 8):
                if move[i] == "0":
                    move_results[i].append(question_string[i])
                else:
                    move_results[i] = self.rule[question_string[i]][move[i]]
            for a0 in move_results[0]:
                for a1 in move_results[1]:
                    for a2 in move_results[2]:
                        for a3 in move_results[3]:
                            for a4 in move_results[4]:
                                for a5 in move_results[5]:
                                    for a6 in move_results[6]:
                                        for a7 in move_results[7]:
                                            answer = a0 + a1 + a2 + a3 + a4 + a5 + a6 + a7
                                            if equality_check(answer):
                                                re_answers.append(answer)
        return re_answers


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setup_ui(window)
    window.show()
    sys.exit(app.exec_())















