#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Задает пароль пользователя root
    Задает уровень целостности высокий
"""

import os
import sys
import subprocess
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
from __py__.main_window import Ui_MainWindow


class RootUserSettings(QtWidgets.QMainWindow):
    def __init__(self, path_to_img):
        super().__init__()
        ui_main = Ui_MainWindow()
        self.ui_main = ui_main
        ui_main.setupUi(self)
        ui_main.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        ui_main.label.setPixmap(QtGui.QPixmap(path_to_img + "/system-users.png"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(path_to_img + "/system-users.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.show()
        self.act()

    def act(self):
        self.ui_main.pushButton.clicked.connect(self.click_apply)
        self.ui_main.pushButton_2.clicked.connect(self.close)
        self.ui_main.checkBox.clicked.connect(self.click_checkbox)

    def click_apply(self):
        err = 0
        # Задание пароля дял root
        psw = self.ui_main.lineEdit.text().encode()  # Представление в байтовом режиме
        p = subprocess.Popen(['/usr/bin/sudo', 'passwd', 'root'],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        p.stdin.write(psw + b"\n" + psw + b"\n")
        p.stdin.flush()
        p.communicate()
        err = err + p.returncode
        #  Добавление уровня целостности равное 63
        ret = os.system("sudo pdpl-user -i 63 root > /dev/null")
        err = err + ret
        if err == 0:
            msgbox_info()
        else:
            msgbox_critical("Ошибка!")

    def click_checkbox(self):
        if self.ui_main.checkBox.isChecked() is True:
            self.ui_main.lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        elif self.ui_main.checkBox.isChecked() is False:
            self.ui_main.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)


def msgbox_critical(text):
    msg = QMessageBox()
    msg.setWindowTitle("Ошибка")
    msg.setText("%s" % text)
    msg.setIcon(QMessageBox.Critical)
    msg.exec_()


def msgbox_info():
    msg = QMessageBox()
    msg.setWindowTitle("Выполнено")
    msg.setText("Выполнено успешно")
    msg.setIcon(QMessageBox.Information)
    msg.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    img_path = sys.path[0] + "/__img__"  # Каталог с изображениями
    rus = RootUserSettings(img_path)
    sys.exit(app.exec_())
