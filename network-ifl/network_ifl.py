#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Программа для работы с Image For Linux по сети
"""


from __py__.main_window import Ui_MainWindow
from __py__.scanner_window import Ui_ScannerWindow
from __py__.auth_window import Ui_Dialog
from __py__.network_scanner import NetworkScanner
#  from __py__.access_scanner import AccessScanner
#  from __py__.ifl_install import IflNetworkInstall
from __py__.view_and_install_deb_packets import find_deb, DebInstall
import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QMessageBox
import threading
import subprocess

file_path = sys.path[0] + "/__file__/"  # Каталог с файлами


class NetWorkIFL(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.child = None
        self.item_number = None
        self.a = None
        self.aw = None
        self.code = None
        self.name_host = None
        #  Инициализация окна сканера
        self.sw = Scanner(self)
        #  Инициализация окна проверки доступа к хостам
        #  self.aw = Access(self)
        #  Инициализация основноого окно
        self.setupUi(self)
        self.creating_list()
        #  Задание параметров treeWidget
        self.treeWidget.setFocusPolicy(Qt.NoFocus)
        self.treeWidget.setIndentation(2)
        self.treeWidget.setColumnWidth(0, 30)
        self.treeWidget.setColumnWidth(1, 150)
        self.act()

    def act(self):
        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.click_pushbutton_2)
        self.action.triggered.connect(self.click_menu_scan)
        self.action_2.triggered.connect(self.click_menu_access)

    def click_menu_scan(self):
        #  Открытие (показ) окна сканера
        self.sw.show()

    def click_menu_access(self):
        #  Инициализация окна проверки доступа к хостам
        self.aw = PasswordRoot(self, "get_check")
        self.aw.show()

    def creating_list(self):
        i = 0
        if os.path.isfile(file_path + "list.txt"):
            with open(file_path + "list.txt", 'r') as f:
                self.treeWidget.clear()
                for line in f:
                    child = QtWidgets.QTreeWidgetItem(self.treeWidget)
                    child.setCheckState(0, Qt.Unchecked)
                    child.setText(1, line.split()[0])
                    try:
                        child.setText(2, line.split()[1])
                    except IndexError:
                        pass
                    i += 1

    def click_pushbutton_2(self):
        #  for item_number in range(self.treeWidget.topLevelItemCount()):
        #      if self.treeWidget.topLevelItem(item_number).checkState(0) == 2:
        self.aw = PasswordRoot(self, "starting")
        self.aw.show()

    def run_ifl(self, password, user_name):
        for item_number in range(self.treeWidget.topLevelItemCount()):
            if self.treeWidget.topLevelItem(item_number).checkState(0) == 2:
                ip = self.treeWidget.topLevelItem(item_number).text(1)
                ini = IflNetworkInstall(ip, password, user_name, file_path + "/ImageForLinux.tar.gz")
                ini.start()

    #  Функция опрашивает отмеченные хосты на доступ к ним
    def get_check(self, password, user_name):
        for item_number in range(self.treeWidget.topLevelItemCount()):
            if self.treeWidget.topLevelItem(item_number).checkState(0) == 2:
                self.item_number = item_number
                ip = self.treeWidget.topLevelItem(item_number).text(1)
                self.access_check(ip, password, user_name)
                self.add_state_tree_widget()
                if self.code == 0:
                    self.get_name()
                    self.treeWidget.topLevelItem(self.item_number).setText(2, self.name_host)

    #  Определение возможности доступа к у даленному хосту
    def access_check(self, ip, password, user_name):
        self.a = AccessScanner(ip, password, user_name)
        self.code = self.a.get_access()

    #  Заполняет поле состояние статусом доступности
    def add_state_tree_widget(self):
        if self.code == 0:
            self.treeWidget.topLevelItem(self.item_number).setText(3, "Доступен")
        elif self.code == 1:
            self.treeWidget.topLevelItem(self.item_number).setText(3, "Ошибка аутентификации")
        elif self.code == 2:
            self.treeWidget.topLevelItem(self.item_number).setText(3, "Ошибка подключения по SSH")
        elif self.code == 3:
            self.treeWidget.topLevelItem(self.item_number).setText(3, "Ошибка подключения")
        elif self.code == 4:
            self.treeWidget.topLevelItem(self.item_number).setText(4, "Ошибка")

    #  Получение имени удаленного хоста
    def get_name(self):
        self.name_host = self.a.get_name()


#  Окно сканера (ввод ip адресов)
class Scanner(QtWidgets.QWidget, Ui_ScannerWindow):
    def __init__(self, root):
        super().__init__()
        self.main = root
        self.setupUi(self)
        self.start_eth = None
        self.finish_eth = None
        self.act()

    def act(self):
        self.pushButton_2.clicked.connect(self.close)
        self.pushButton.clicked.connect(self.get_ip)

    def get_ip(self):
        self.start_eth = self.lineEdit.text()
        self.finish_eth = self.lineEdit_2.text()
        self.run_scan()

    def run_scan(self):
        ns = NetworkScanner(self.start_eth, self.finish_eth, file_path + "list.txt")
        ns.start()
        msg = TimerMessageBox()
        msg.exec_()
        self.main.creating_list()
        self.close()


class PasswordRoot(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, main, action):
        super().__init__()
        self.main = main
        self.action = action
        self.root_pass = None
        self.ul = []  # Список пользователей
        self.user_name = None   # Выбранный пользователь
        self.setupUi(self)
        self.user_list()
        self.act()
        self.setModal(True)
        self.pushButton.setCheckable(True)

    def user_list(self):
        proc = subprocess.run("sudo cat /etc/passwd | grep '/bin/bash' | awk -F: '{print $1}'", shell=True,
                              stdout=subprocess.PIPE)
        for line in proc.stdout.split():
            if line:
                self.ul.append(line.decode("utf-8"))
        self.add_combobox()

    def add_combobox(self):
        self.comboBox.addItems(self.ul)

    def act(self):
        self.pushButton.clicked.connect(self.get_password)

    def get_password(self):
        self.pushButton.setCheckable(False)
        self.root_pass = self.lineEdit_2.text()
        self.user_name = self.comboBox.currentText()
        if self.action == "get_check":
            self.main.get_check(self.root_pass, self.user_name)
        elif self.action == "starting":
            self.main.run_ifl(self.root_pass, self.user_name)
        self.close()


#  Окно таймер выполнения сканирования сети
#  Окно автоматически закрывается после завершения сканирования
class TimerMessageBox(QMessageBox, threading.Thread):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("wait")
        self.time_to_wait = 0
        self.setText("wait (closing automatically) running in {0} second.".format(self.time_to_wait))
        self.setStandardButtons(QMessageBox.NoButton)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.change_content)
        self.timer.start()

    def change_content(self):
        self.setText("wait (closing automatically) running in {0} second.".format(self.time_to_wait))
        self.time_to_wait += 1
        if threading.activeCount() == 1:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()


def unpack(path):
    tar_gz_arch = path + "/paramiko.tar.gz"
    print(tar_gz_arch)
    proc = subprocess.Popen("tar xvzf %s" % tar_gz_arch, shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    proc.communicate()
    return proc.returncode


def find_and_install_module_paramiko():
    res = find_deb("python3-paramiko")
    if res != 0:
        res = unpack(sys.path[0] + "/__dis__")
        if res == 0:
            ins = DebInstall("paramiko/*")
            ins.start()
            msg = TimerMessageBox()
            msg.exec_()
            os.system("rm -rf paramiko")
            return ins.err_proc
    else:
        return 0


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    err_find = find_and_install_module_paramiko()
    if err_find == 0:
        from __py__.access_scanner import AccessScanner
        from __py__.ifl_install import IflNetworkInstall
        nw = NetWorkIFL()
        nw.show()
    else:
        print("Ошибка!")
        sys.exit()
    sys.exit(app.exec_())
