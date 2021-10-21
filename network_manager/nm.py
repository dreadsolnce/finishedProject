#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Программа отключающая Network Manager
"""

import sys
import subprocess
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
from __py__.main import Ui_Dialog


class NetworkManager(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, path_to_img):
        super().__init__()
        ui = Ui_Dialog()
        self.ui = ui
        ui.setupUi(self)
        ui.label_2.setPixmap(QtGui.QPixmap(path_to_img + "/network-wired-activated.png"))
        self.show()
        self.act()

    def act(self):
        self.ui.pushButton.clicked.connect(self.enable_nm)
        self.ui.pushButton_2.clicked.connect(self.disable_nm)

    def enable_nm(self):
        process = subprocess.Popen("sudo systemctl --now unmask NetworkManager",
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        _, err = process.communicate()
        if process.returncode != 0:
            QMessageBox.critical(self, "Ошибка", "Ошибка включения службы")
            exit(255)

        process = subprocess.Popen("sudo mv -f /etc/xdg/autostart/nm-applet.desktop.disabled "
                                   "/etc/xdg/autostart/nm-applet.desktop",
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        _, err = process.communicate()
        if process.returncode != 0:
            QMessageBox.critical(self, "Ошибка", "Ошибка добавления значка")
            exit(255)

        process = subprocess.Popen("sudo systemctl restart NetworkManager",
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        _, err = process.communicate()
        if process.returncode != 0:
            QMessageBox.critical(self, "Ошибка", "Ошибка перезапуска сетевой службы")
            exit(255)

        ask = QMessageBox.information(self, "", "Перезапустить графическую сесию?",
                                QMessageBox.Cancel | QMessageBox.Ok, QMessageBox.Cancel)
        if ask == QMessageBox.Ok:
            process = subprocess.Popen("sudo systemctl restart fly-dm",
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            _, err = process.communicate()
            if process.returncode != 0:
                QMessageBox.critical(self, "Ошибка", "Ошибка перезапуска графической сесии")
                exit(255)

        QMessageBox.information(self, "Сообщение!", "Успех!")

    def disable_nm(self):
        process = subprocess.Popen("sudo systemctl --now mask NetworkManager",
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        _, err = process.communicate()
        if process.returncode != 0:
            QMessageBox.critical(self, "Ошибка", "Ошибка отключения службы")
            exit(255)

        process = subprocess.Popen("sudo mv -f /etc/xdg/autostart/nm-applet.desktop "
                                   "/etc/xdg/autostart/nm-applet.desktop.disabled",
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        _, err = process.communicate()
        if process.returncode != 0:
            QMessageBox.critical(self, "Ошибка", "Ошибка удаления значка")
            exit(255)

        process = subprocess.Popen("sudo systemctl restart networking",
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        _, err = process.communicate()
        if process.returncode != 0:
            QMessageBox.critical(self, "Ошибка", "Ошибка перезапуска сетевой службы")
            exit(255)

        ask = QMessageBox.information(self, "", "Перезапустить графическую сесию?",
                                      QMessageBox.Cancel | QMessageBox.Ok, QMessageBox.Cancel)
        if ask == QMessageBox.Ok:
            process = subprocess.Popen("sudo systemctl restart fly-dm",
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            _, err = process.communicate()
            if process.returncode != 0:
                QMessageBox.critical(self, "Ошибка", "Ошибка перезапуска графической сесии")
                exit(255)

        QMessageBox.information(self, "Сообщение!", "Успех!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    img_path = sys.path[0] + "/__img__"  # Каталог с изображениями
    n = NetworkManager(img_path)
    sys.exit(app.exec_())
