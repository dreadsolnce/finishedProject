#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Программа включения и отключения автовхода в систему
"""
import sys
import subprocess
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtWidgets import QMessageBox
from __py__.main import Ui_MainWindow
from __py__.replace_string import change_string


class AutoLoginUser(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ul = []        # Список пользователей
        self.ml = []        # Список с уровнями целостности
        self.setupUi(self)
        self.user_list()
        self.user_mac()

        self.comboBox.currentTextChanged.connect(self.user_mac)
        self.pushButton.clicked.connect(self.clicked_enable)
        self.pushButton_2.clicked.connect(self.clicked_disable)

    def user_list(self):
        proc = subprocess.run("sudo cat /etc/passwd | grep '/bin/bash' | awk -F: '{print $1}'", shell=True,
                              stdout=subprocess.PIPE)
        for line in proc.stdout.split():
            if line:
                self.ul.append(line.decode("utf-8"))
        self.add_combobox()

    def user_mac(self):
        name_user = self.comboBox.currentText()
        self.ml.clear()
        proc = subprocess.run("sudo pdpl-user " + name_user + " | awk '{print $1}' | awk -F: '{print $2}'", shell=True,
                              stdout=subprocess.PIPE)
        for line in proc.stdout.split():
            if line:
                self.ml.append(line.decode("utf-8"))
        self.add_combobox_2()

    def add_combobox(self):
        self.comboBox.addItems(self.ul)

    def add_combobox_2(self):
        self.comboBox_2.clear()
        self.comboBox_2.addItems(self.ml)

    def clicked_enable(self):
        if self.comboBox.currentText() == "root":
            QMessageBox.warning(self, 'Предупреждение', "Для пользователя root нельзя включить автовход!",
                                QMessageBox.Close)
        else:
            f_autostart = "/etc/X11/fly-dm/fly-dmrc"

            change_string(f_autostart, "AutoLoginEnable", "AutoLoginEnable=true")
            change_string(f_autostart, "AutoLoginUser", "AutoLoginUser="+self.comboBox.currentText())
            change_string(f_autostart, "AutoLoginMAC", "AutoLoginMAC=0:"+self.comboBox_2.currentText()+":0")

            QMessageBox.information(self, 'Статус', "Выполнено!", QMessageBox.Close)

    def clicked_disable(self):
        f_autostart = "/etc/X11/fly-dm/fly-dmrc"

        change_string(f_autostart, "AutoLoginEnable", "AutoLoginEnable=false")
        change_string(f_autostart, "AutoLoginUser", "#AutoLoginUser=alex1")
        change_string(f_autostart, "AutoLoginMAC", "#AutoLoginMAC=")

        QMessageBox.information(self, 'Статус', "Выполнено!", QMessageBox.Close)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    alu = AutoLoginUser()
    alu.show()
    sys.exit(app.exec_())
