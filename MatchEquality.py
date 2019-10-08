import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import numpy as np
import cv2
import json


class MainWindow(object):
    def __init__(self):
        self.centralWidget = None
        self.main_window = None
        # 组件
        self.button_open = None

    def setup_ui(self, main_window):
        self.main_window = main_window
        self.main_window.setObjectName("mainWindow")
        self.main_window.setWindowModality(QtCore.Qt.WindowModal)
        self.main_window.setFixedSize(1280, 720)

        # 按钮
        self.centralWidget = QtWidgets.QWidget(self.main_window)
        self.centralWidget.setObjectName("centralWidget")
        # 打开
        self.button_open = QtWidgets.QPushButton(self.centralWidget)
        self.button_open.setGeometry(QtCore.QRect(20, 500, 120, 40))
        self.button_open.setObjectName("button_open")
        self.button_open.setText("打开")
        #self.button_open.clicked.connect(self.button_open_click)

        self.main_window.setCentralWidget(self.centralWidget)
        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.main_window.setWindowTitle(_translate("mainWindow", "移动火柴"))


if __name__ == "__main__":

    f = open('./data/rule.json', encoding='utf-8')
    res = f.read()
    rule = json.loads(res)
    f.close()

    def opop(op):
        if op == "+1":
            return "-1"
        if op == "-1":
            return "+1"
        if op == "=1":
            return "=1"
        if op == "+2":
            return "-2"
        if op == "-2":
            return "+2"
        if op == "=2":
            return "=2"
        if op == "-=1":
            return "+=1"
        if op == "+=1":
            return "-=1"



    for number1 in rule.keys():
        for operation in rule[number1].keys():
            for number2 in rule[number1][operation]:
                if number1 in rule[number2][opop(operation)]:
                    pass
                else:
                    print(number1)
                    print(operation)
                    print(number2)
                    print("-------------")



    print(rule)

    with open("./data/rule.json", "w") as f:
        json.dump(rule, f)

    '''
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setup_ui(window)
    window.show()
    sys.exit(app.exec_())
    
    '''












