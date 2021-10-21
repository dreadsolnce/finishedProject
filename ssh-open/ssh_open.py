#!/usr/bin/env python3
# -*- coding:utf-8 -*-


"""
    Включает доступ по протоколу ssh для пользователя с root правами
    а также механизм, позволяющий отображать на локальном клиентском
    компьютере графические интерфейсы X11 программ, запущенных на
    удаленном сервере.
"""

import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from __py__.main import Ui_MainWindow
from __py__.replace_string import change_string


# Определение переменных окружения или рабочих путей
def myenvironment(type_exec):
    if type_exec == "main_module":
        img_path = sys.path[0] + "/__img__"  # Каталог с изображениями
        print("Каталог с изображениями = %s" % img_path)


# Применить настройки конфигурации
def apply():
    ret = msgbox_ask("Вы уверены, что хотите применить настройки?")
    if ret == QMessageBox.Ok:
        f_ssh = "/etc/ssh/ssh_config"
        f_sshd = "/etc/ssh/sshd_config"
        change_string(f_ssh, "ForwardX11", "ForwardX11 yes")
        change_string(f_sshd, "PermitRootLogin", "PermitRootLogin yes")
        change_string(f_sshd, "AddressFamily", "AddressFamily inet")
        change_string(f_sshd, "X11UseLocalhost", "X11UseLocalhost yes")
        os.system("sudo systemctl start ssh")
        os.system("sudo systemctl enable ssh")


# Отмена внесенных изменений с помощью бэкапа файлов
def discard():
    ret = msgbox_ask("Вы уверены, что хотите сбросить настройки в "
                     "значение по умолчанию?")
    if ret == QMessageBox.Ok:
        f_ssh = "/etc/ssh/ssh_config"
        f_sshd = "/etc/ssh/sshd_config"
        hit_count = False
        if os.path.isfile(f_ssh + ".PNO.bak"):
            os.system("sudo cp -R " + f_ssh + ".PNO.bak " + f_ssh)
        elif not os.path.isfile(f_ssh + ".PNO.bak"):
            hit_count = True
        if os.path.isfile(f_sshd + ".PNO.bak"):
            os.system("sudo cp -R " + f_sshd + ".PNO.bak " + f_sshd)
        elif not os.path.isfile(f_sshd + ".PNO.bak"):
            hit_count = True
        if hit_count is True:
            msgbox_critical("Не найдена копия исходного файла!")


# Главное окно программы, вызываемое из файла main.py
def main_win():
    global main
    main = QtWidgets.QMainWindow()
    ui_main = Ui_MainWindow()
    ui_main.setupUi(main)
    main.show()
    ui_main.pushButton.clicked.connect(apply)
    ui_main.pushButton_2.clicked.connect(discard)
    ui_main.pushButton_3.clicked.connect(main.close)


def msgbox_ask(text):
    msg = QMessageBox()
    msg.setWindowTitle("Confirmation")
    msg.setText(text)
    msg.setIcon(QMessageBox.Information)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    ret = msg.exec_()  # Значение нажатой кнопки
    return ret


def msgbox_critical(text):
    msg = QMessageBox()
    msg.setWindowTitle("Ошибка!")
    msg.setText(text)
    msg.setIcon(QMessageBox.Critical)
    msg.exec_()


if __name__ == "__main__":
    global main
    myenvironment("main_module")  # Запущен как главная программа
    app = QtWidgets.QApplication(sys.argv)
    main_win()
    sys.exit(app.exec_())
