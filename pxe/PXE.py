#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Программа для запуска PXE сервера
"""

from __py__.main_window_pxe import Ui_MainWindow
from __py__.two_window_pxe import Ui_MainWindow_2
from __py__.FindEthernet import find_ethernet
from __py__.MChangeFile import WriteStringFile, FindTemplate, ReplaceTemplate, AddStringFile, DelString
import sys
import os
import subprocess
import shutil
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox

file_path = sys.path[0] + "/__file__/"  # Каталог с файлами


class PXE(QtWidgets.QMainWindow, Ui_MainWindow, Ui_MainWindow_2):
    def __init__(self, path_to_img):
        super().__init__()
        self.path_to_img = path_to_img
        self.file_pxe = None
        self.auto = None
        self.desktop = None
        self.eth = None
        self.path_to_pxe = None
        #  Инициализация основноого окно
        ui_main = Ui_MainWindow()
        self.ui_main = ui_main
        ui_main_2 = Ui_MainWindow_2()
        self.ui_main_2 = ui_main_2
        ui_main.setupUi(self)
        ui_main.label.setPixmap(QtGui.QPixmap(path_to_img + "/PXE-Logo.png"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(path_to_img + "/PXE-Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.show()
        self.act()

    def act(self):
        self.ui_main.pushButton.clicked.connect(self.click_pushbutton_2)
        self.ui_main.pushButton_2.clicked.connect(self.close)

    def click_pushbutton_2(self):
        self.close()
        self.init_window_2()

    def init_window_2(self):
        #  Инициализация второго окна
        self.ui_main_2.setupUi(self)
        self.ui_main_2.label.setPixmap(QtGui.QPixmap(self.path_to_img + "/PXE-Logo.png"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.path_to_img + "/PXE-Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.view_ethernet()
        self.show()
        self.act_2()

    def act_2(self):
        self.ui_main_2.pushButton.clicked.connect(self.click_pushbutton_2_2)
        self.ui_main_2.pushButton_2.clicked.connect(self.close)
        self.ui_main_2.checkBox_3.clicked.connect(self.clicked_checkbox_3)
        self.ui_main_2.checkBox_4.clicked.connect(self.clicked_checkbox_4)
        self.ui_main_2.pushButton_3.clicked.connect(self.clicked_pushbutton_3_2)

    def click_pushbutton_2_2(self):
        if self.ui_main_2.checkBox_3.isChecked():
            self.param_pxe()
        elif self.ui_main_2.checkBox_4.isChecked():
            self.uninstall_pxe()

    def clicked_checkbox_3(self):
        if self.ui_main_2.checkBox_3.isChecked():  # Установить
            self.ui_main_2.checkBox.setEnabled(True)  # Автостарт
            self.ui_main_2.checkBox_2.setEnabled(True)  # Ярлыки
            self.ui_main_2.comboBox.setEnabled(True)  # Сетевой интерфейс
            self.ui_main_2.pushButton_3.setEnabled(True)  # Путь
            self.ui_main_2.lineEdit.setEnabled(True)
            self.ui_main_2.checkBox_4.setDisabled(True)  # Удалить
        else:
            self.ui_main_2.checkBox.setEnabled(False)
            self.ui_main_2.checkBox_2.setEnabled(False)
            self.ui_main_2.comboBox.setEnabled(False)
            self.ui_main_2.pushButton_3.setEnabled(False)
            self.ui_main_2.lineEdit.setEnabled(False)
            self.ui_main_2.checkBox_4.setDisabled(False)

    def clicked_checkbox_4(self):  # Удалить
        if self.ui_main_2.checkBox_4.isChecked():
            self.ui_main_2.checkBox_3.setDisabled(True)
        else:
            self.ui_main_2.checkBox_3.setDisabled(False)

    def view_ethernet(self):
        i = 0
        out = find_ethernet()
        for s in out:
            self.ui_main_2.comboBox.addItem("")
            self.ui_main_2.comboBox.setItemText(i, s.strip())
            i += 1

    def clicked_pushbutton_3_2(self):
        self.file_pxe = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        self.ui_main_2.lineEdit.setText(self.file_pxe)

    def param_pxe(self):
        self.eth = self.ui_main_2.comboBox.currentText()
        if self.ui_main_2.checkBox.isChecked():
            self.auto = "enable"
        elif not self.ui_main_2.checkBox.isChecked():
            self.auto = "disable"
        if self.ui_main_2.checkBox_2.isChecked():
            self.desktop = "enable"
        elif not self.ui_main_2.checkBox.isChecked():
            self.desktop = "disable"
        self.path_to_pxe = self.ui_main_2.lineEdit.text()

        if os.path.isfile(self.path_to_pxe) and self.path_to_pxe:
            self.inst_pxe()

    def inst_pxe(self):
        e = self.copy_qemu_pnosko()
        if e != 0:
            exit(255)
        e = self.copy_start_pxe()
        if e != 0:
            exit(255)
        if self.auto == "enable":
            self.copy_auto()
        if self.desktop == "enable":
            self.copy_desktop()
        QMessageBox.information(self, "Info", "Успешно!")

    def copy_qemu_pnosko(self):
        process = subprocess.Popen("sudo cp " + sys.path[0] + "/__file__/qemu-if* /etc/",
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        _, err = process.communicate()
        if process.returncode != 0:
            QMessageBox.critical(self, "Ошибка", "Ошибка копирования файлов qemu-if*.PNOSKO в /etc/")
        return process.returncode

    def copy_start_pxe(self):
        process = subprocess.Popen("sudo cp " + sys.path[0] + "/__file__/StartPXE.py /usr/local/bin/StartPXE.py",
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        _, err = process.communicate()
        if process.returncode != 0:
            QMessageBox.critical(self, "Ошибка", "Ошибка копирования StartPXE.py в /usr/local/bin")
        return process.returncode

    def copy_auto(self):
        if not os.path.isfile("/home/" + os.getlogin() + "/.xsessionrc"):
            WriteStringFile("exec /usr/local/bin/StartPXE.py " + self.eth + " '" + self.file_pxe + "' &",
                            "/home/" + os.getlogin() + "/.xsessionrc")
        elif os.path.isfile("/home/" + os.getlogin() + "/.xsessionrc"):
            e = FindTemplate("/home/" + os.getlogin() + "/.xsessionrc", "/usr/local/bin/StartPXE.py")
            if e.exit_code == 0:  # Шаблон найден
                if not os.path.isfile("/home/" + os.getlogin() + "/.xsessionrc.bak.PNOSKO"):
                    try:
                        shutil.copyfile("/home/" + os.getlogin() + "/.xsessionrc",
                                        "/home/" + os.getlogin() + "/.xsessionrc.bak.PNOSKO")
                    except PermissionError as e:
                        QMessageBox.critical(self, "Ошибка", str(e))
                        exit(255)
                e = ReplaceTemplate("/home/" + os.getlogin() + "/.xsessionrc",
                                    "/usr/local/bin/StartPXE.py",
                                    "exec /usr/local/bin/StartPXE.py " + self.eth + " '" + self.file_pxe + "' &")
                if e.exit_code != 0:
                    QMessageBox.critical(self, "Ошибка", "Ошибка изменения файла .xsessionrc")
                    exit(255)
            elif e.exit_code == -1:  # Шаблон не найден
                if not os.path.isfile("/home/" + os.getlogin() + "/.xsessionrc.bak.PNOSKO"):
                    try:
                        shutil.copyfile("/home/" + os.getlogin() + "/.xsessionrc",
                                        "/home/" + os.getlogin() + "/.xsessionrc.bak.PNOSKO")
                    except PermissionError as e:
                        QMessageBox.critical(self, "Ошибка", str(e))
                        exit(255)
                e = AddStringFile("exec /usr/local/bin/StartPXE.py " + self.eth + " '" + self.file_pxe + "' &",
                                  "/home/" + os.getlogin() + "/.xsessionrc")
                if e.exit_code != 0:
                    QMessageBox.critical(self, "Ошибка", "Ошибка изменения файла .xsessionrc")
                    exit(255)

    def copy_desktop(self):
        # Копируем иконку
        if not os.path.isdir("/home/" + os.getlogin() + "/.local/share/icons"):
            try:
                os.mkdir("/home/" + os.getlogin() + "/.local/share/icons")
                shutil.copyfile(sys.path[0] + "/__img__/qemu_start.png",
                                "/home/" + os.getlogin() + "/.local/share/icons/qemu_start.png")
            except PermissionError as e:
                QMessageBox.critical(self, "Ошибка", str(e))
                exit(255)

        # Копируем ярлык
        if not os.path.isfile("/home/" + os.getlogin() + "/Desktop/start_pxe.desktop"):
            try:
                shutil.copyfile(sys.path[0] + "/__file__/start_pxe.desktop",
                                "/home/" + os.getlogin() + "/Desktop/start_pxe.desktop")
            except PermissionError as e:
                QMessageBox.critical(self, "Ошибка", str(e))
                exit(255)
        e = ReplaceTemplate("/home/" + os.getlogin() + "/Desktop/start_pxe.desktop", "Exec",
                            "Exec=/usr/local/bin/StartPXE.py " + self.eth + " '" + self.file_pxe + "'")
        if e.exit_code != 0:
            QMessageBox.critical(self, "Ошибка", "Ошибка создания ярлыка!")
            exit(255)

    def uninstall_pxe(self):
        if os.path.isfile("/etc/qemu-ifup.PNOSKO"):
            process = subprocess.Popen("sudo rm -rf /etc/qemu-ifup.PNOSKO",
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            _, err = process.communicate()
            if process.returncode != 0:
                QMessageBox.critical(self, "Ошибка", "Ошибка удаления файла /etc/qemu-ifup.PNOSKO")
                # exit(255)
        if os.path.isfile("/etc/qemu-ifdown.PNOSKO"):
            process = subprocess.Popen("sudo rm -rf /etc/qemu-ifdown.PNOSKO",
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            _, err = process.communicate()
            if process.returncode != 0:
                QMessageBox.critical(self, "Ошибка", "Ошибка удаления файла /etc/qemu-ifup.PNOSKO")
                # exit(255)
        if os.path.isfile("/usr/local/bin/StartPXE.py"):
            process = subprocess.Popen("sudo rm -rf /usr/local/bin/StartPXE.py",
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            _, err = process.communicate()
            if process.returncode != 0:
                QMessageBox.critical(self, "Ошибка", "Ошибка удаления файла StartPXE.py в /usr/local/bin/StartPXE.py")
                # exit(255)
        if os.path.isfile("/home/" + os.getlogin() + "/.xsessionrc"):
            e = DelString("/home/" + os.getlogin() + "/.xsessionrc", "/usr/local/bin/StartPXE.py")
            if e.exit_code == 1:
                QMessageBox.critical(self, "Ошибка", "Ошибка удаления из автозагрузки!")
                # exit(255)
        if os.path.isfile("/home/" + os.getlogin() + "/Desktop/start_pxe.desktop"):
            try:
                os.remove("/home/" + os.getlogin() + "/Desktop/start_pxe.desktop")
            except PermissionError as e:
                QMessageBox.critical(self, "Ошибка", str(e))
                # exit(255)
        QMessageBox.information(self, "Info", "Успешно!")
        # cl = EmptyLine("/home/" + os.getlogin() + "/.xsessionrc")
        # print(cl.exit_code)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    img_path = sys.path[0] + "/__img__"  # Каталог с изображениями
    p = PXE(img_path)
    sys.exit(app.exec_())
