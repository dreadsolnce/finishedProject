#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TwoWindowInstallUninstall.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QDesktopWidget

class Ui_TwoWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(319, 175)
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
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 3, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(213, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 319, 21))
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

        self.comboBox.currentIndexChanged.connect(self.clicked_combobox_two_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Установка программы TimeShift"))
        self.pushButton.setText(_translate("MainWindow", "Применить"))
        self.pushButton_2.setText(_translate("MainWindow", "Отмена"))
        self.label_2.setText(_translate("MainWindow", "Действие:"))
        self.comboBox.setItemText(0, _translate("MainWindow", "--- Выберите действие ---"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Установить"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Удалить"))

    # Моя функция отслеживания изменения combobox
    def clicked_combobox_two_window(self):
        if self.comboBox.currentIndex() == 0:
            self.pushButton.setEnabled(False)
        elif self.comboBox.currentIndex() == 1 or self.comboBox.currentIndex() == 2:
            self.pushButton.setEnabled(True)

def MyEnvironment(path_module):
    global img_path
    if path_module == "main_module":  # Запущен как главная программа
        img_path = sys.path[0].rpartition('__py__')[0] + "/__img__"  # Каталог с изображениями
    else:  # запущен как зависимый модуль
        img_path = sys.path[0] + "/__img__"  # Каталог с изображениями

if __name__ == "__main__":
    MyEnvironment("main_module")  # Запущен как главная программа
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_TwoWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
else:
    MyEnvironment("dependent_module")  # запущен как зависимый модуль
