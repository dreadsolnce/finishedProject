# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(736, 280)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(img_path + "/ssh-windows-min.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(96, 104))
        self.label.setMaximumSize(QtCore.QSize(96, 16777215))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(img_path + "/ssh-windows-min.png"))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 1, 1, 1, 3)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 2, 0, 1, 4)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 3, 2, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 3, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Доступ по SSH"))
        self.label_2.setText(_translate("MainWindow", "Краткое описание"))
        self.textEdit.setHtml(_translate("MainWindow",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-style:italic;\">Данный скрипт открывает доступ по протоколу SSH для пользователя с правами root.</span></p>\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Краткое описание:</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">   <span style=\" font-size:12pt; font-weight:600; color:#000000;\">PermitRootLogin yes</span><span style=\" font-size:11pt;\"> - разрешаем заходить по ssh руту.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">   </span><span style=\" font-size:12pt; font-weight:600; color:#000000;\">ForwardX11 yes</span><span style=\" font-size:11pt;\"> - это механизм, позволяющий отображать на локальном клиентском компьютере графические интерфейсы X11 программ, запущенных на удаленном сервере (на сервере должна быть включена опция X11Forwarding yes). SSH имеет возможность безопасного туннелирования X11 соеденений, так что сеансы X11 forfarding-а шифруются и инкапсулируются.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-style:italic;\">   </span><span style=\" font-size:12pt; font-weight:600; color:#000000;\">AddressFamily inet</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#000000;\">   X11UseLocalhost yes </span><span style=\" font-size:11pt;\">- данные два параметра отвечают за запуск графической программы через протокол ssh на локальной машине. Другими словами запуск программы установленной на локальной машине через ssh.</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Открыть доступ"))
        self.pushButton.setText(_translate("MainWindow", "Открыть доступ"))
        self.pushButton_2.setText(_translate("MainWindow", "Сбросить"))
        self.pushButton_3.setText(_translate("MainWindow", "Выход"))

# Определение переменных окружения или рабочих путей
def myenvironment(type_exec):
    global img_path
    if type_exec == "main_module":
        img_path = sys.path[0].rpartition('__py__')[0] + "__img__"  # Каталог с изображениями
        print (img_path)
    elif type_exec == "dependent_module":  # запущен как зависимый модуль
        img_path = sys.path[0] + "/__img__"  # Каталог с изображениями


if __name__ == "__main__":
    myenvironment("main_module")  # Запущен как главная программа
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
else:
    myenvironment("dependent_module")  # запущен как зависимый модуль