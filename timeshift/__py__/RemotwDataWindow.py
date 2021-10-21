# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RemotwDataWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QDesktopWidget

class Ui_DataForRemote(object):
    def setupUi(self, DataForRemote):
        DataForRemote.setObjectName("DataForRemote")
        DataForRemote.resize(582, 222)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(img_path + "/timeshift.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DataForRemote.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(DataForRemote)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(DataForRemote)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setMinimumSize(QtCore.QSize(0, 0))
        self.label_2.setMaximumSize(QtCore.QSize(181, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setMinimumSize(QtCore.QSize(331, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setMaximumSize(QtCore.QSize(181, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(331, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setMaximumSize(QtCore.QSize(181, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(331, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEdit_3.setAcceptDrops(True)
        self.lineEdit_3.setAutoFillBackground(True)
        self.lineEdit_3.setReadOnly(False)
        self.lineEdit_3.setPlaceholderText("")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_2.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.frame, 1, 0, 1, 3)
        self.label = QtWidgets.QLabel(DataForRemote)
        self.label.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)
        self.pushButton = QtWidgets.QPushButton(DataForRemote)
        self.pushButton.setMaximumSize(QtCore.QSize(101, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(DataForRemote)
        self.pushButton_2.setMaximumSize(QtCore.QSize(101, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 3, 2, 1, 1)
        self.line = QtWidgets.QFrame(DataForRemote)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 0, 1, 3)

        self.retranslateUi(DataForRemote)
        QtCore.QMetaObject.connectSlotsByName(DataForRemote)

        # Окно по центру
        qr = DataForRemote.frameGeometry()
        qp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(qp)
        DataForRemote.move(qr.topLeft())

    def retranslateUi(self, DataForRemote):
        _translate = QtCore.QCoreApplication.translate
        DataForRemote.setWindowTitle(_translate("DataForRemote", "Данные для удаленного подключения"))
        self.label_2.setText(_translate("DataForRemote", "Имя пользователя:"))
        self.label_3.setText(_translate("DataForRemote", "Пароль пользователя:"))
        self.label_4.setText(_translate("DataForRemote", "IP адрес:"))
        self.lineEdit_3.setInputMask(_translate("DataForRemote", "000.000.000.000;_"))
        self.label.setText(_translate("DataForRemote", "Данные для удаленного подключения"))
        self.pushButton.setText(_translate("DataForRemote", "Применить"))
        self.pushButton_2.setText(_translate("DataForRemote", "Отмена"))

def MyEnvironment(path_module):
    global img_path
    if path_module == "main_module":  # Запущен как главная программа
        img_path = sys.path[0].rpartition('__py__')[0] + "/__img__"  # Каталог с изображениями
    else:  # запущен как зависимый модуль
        img_path = sys.path[0] + "/__img__"  # Каталог с изображениями

if __name__ == "__main__":
    MyEnvironment("main_module")  # Запущен как главная программа
    app = QtWidgets.QApplication(sys.argv)
    DataForRemote = QtWidgets.QWidget()
    ui = Ui_DataForRemote()
    ui.setupUi(DataForRemote)
    DataForRemote.show()
    sys.exit(app.exec_())
else:
    MyEnvironment("dependent_module")  # запущен как зависимый модуль