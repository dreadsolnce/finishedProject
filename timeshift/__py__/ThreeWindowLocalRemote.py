#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ThreeWindowLocalRemote.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QDesktopWidget

class Ui_ThreeWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(381, 204)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(img_path + "/timeshift.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAccessibleName("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 1, 0, 1, 3)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setEnabled(False)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 2, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 2, 2, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.checkBox_4 = QtWidgets.QCheckBox(self.frame_2)
        #self.checkBox_4.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_4.setFont(font)
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout_3.addWidget(self.checkBox_4, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.checkBox_3 = QtWidgets.QCheckBox(self.frame_2)
        self.checkBox_3.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setCheckable(True)
        self.checkBox_3.setChecked(False)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout_3.addWidget(self.checkBox_3, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_2, 0, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(213, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 381, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Окно по центру
        qr = MainWindow.frameGeometry()
        qp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(qp)
        MainWindow.move(qr.topLeft())

        self.checkBox_3.clicked.connect(self.clicked_checkbox_two_window)
        self.checkBox_4.clicked.connect(self.clicked_checkbox_two_window)

    # Моя функция отслеживания выбора чекбоксов
    def clicked_checkbox_two_window(self):
        if self.checkBox_3.isChecked() == True:
            self.checkBox_4.setDisabled(True)
            self.pushButton.setEnabled(True)
        elif self.checkBox_4.isChecked() == True:
            self.checkBox_3.setDisabled(True)
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setDisabled(True)
            self.checkBox_3.setDisabled(False)
            self.checkBox_4.setDisabled(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Установка программы TimeShift"))
        self.pushButton.setText(_translate("MainWindow", "Применить"))
        self.pushButton_2.setText(_translate("MainWindow", "Отмена"))
        self.checkBox_4.setText(_translate("MainWindow", "Удаленный компьютер"))
        self.label_3.setText(_translate("MainWindow", "Тип установки:"))
        self.checkBox_3.setText(_translate("MainWindow", "Локальный компьютер"))

def MyEnvironment(path_module):
    global img_path
    if path_module == "main_module":  # Запущен как главная программа
        img_path = sys.path[0].rpartition('__py__')[0] + "/__img__"  # Каталог с изображениями
    else:  # запущен как зависимый модуль
        img_path = sys.path[0] + "/__img__"  # Каталог с изображениями

if __name__ == "__main__":
    MyEnvironment("main_module")  # Запущен как главная программа
    path_prog = sys.path[0].rpartition('__py__')[0] # Каталог запуска программы
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_ThreeWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
else:
    MyEnvironment("dependent_module")  # запущен как зависимый модуль