#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
import os
import shutil
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDesktopWidget
from bginfo import Ui_MainWindow, Ui_Form


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_main = Ui_MainWindow()
        self.ui_choice = None
        self.ui_main.setupUi(self)
#        self.window_center()
        self.show()
        self.act_buttons()

    def act_buttons(self):
        print("Действия над кнопками в главном окне")
        self.ui_main.pushButton.clicked.connect(self.win_get_config)
        self.ui_main.pushButton_2.clicked.connect(act_uninstall)

    def win_get_config(self):
        print("Нажата кнопка установить")
        self.ui_choice = ChoiceConfig()


class ChoiceConfig(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.conf = None
        self.ui_choice = Ui_Form()
        self.ui_choice.setupUi(self)
        self.run_win_choice_config()

    def run_win_choice_config(self):
        print("Окно выбора конфига!")
        self.setModal(True)
        self.show()
        self.act_buttons()

    def act_buttons(self):
        print("Действия над кнопками в окне выбора конфига")
        self.ui_choice.pushButton.clicked.connect(self.act_apply)

    def act_apply(self):
        print("Нажата кнопка применить")
        self.conf = self.ui_choice.comboBox.currentText()
        print("Выбрана конфигурация товарища {0}а".format(self.conf))
        act = Action(action="install", config=self.conf)
        act.act()
        self.close()


class Action(QtWidgets.QDialog):
    PATH_CONFIG = sys.path[0] + "/resources/config/"
    PATH_SCRIPT = sys.path[0] + "/resources/files/"

    def __init__(self, action=None, config=None):
        super().__init__()
        self.action = action
        self.config = config
        self.err = False
        self.src_file = None
        self.path_config = Action.PATH_CONFIG
        print("Каталог с конфигами: " + self.path_config)
        self.path_script = Action.PATH_SCRIPT
        print("Каталог со скриптами: " + self.path_script)

    def window_center(self):
        qr = self.frameGeometry()
        qp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(qp)
        self.move(qr.topLeft())

    def act(self):
        if self.action == "install":
            print("Выполняем установку программы")
            self.install()
        elif self.action == "uninstall":
            print("Выполняем удаление программы")
            self.uninstall()

    def install(self):
        if self.config == "Богданов" and os.path.isfile(self.path_config + "bginfo.bpb.bg"):
            print("Устанавливаем конфигурацию Богданова П.Б.")
            self.src_file = self.path_config + "bginfo.bpb.bg"
        elif self.config == "Колчин" and os.path.isfile(self.path_config + "bginfo.kvl.bg"):
            print("Устанавливаем конфигурацию Колчина В.Л.")
            self.src_file = self.path_config + "bginfo.kvl.bg"
        else:
            self.error("Не найден конфигурационный файл!")

        try:
            if not self.err:
                dist_file = "/usr/local/bin/bginfo.bg"
                shutil.copyfile(self.src_file, dist_file)
                os.chmod(dist_file, 0o777)
                os.system(dist_file + "&")

                src_file = self.path_script + "bginfo.desktop"
                dist_file = "/etc/xdg/autostart/bginfo.desktop"
                shutil.copyfile(src_file, dist_file)

                self.window_center()
                QMessageBox.information(self, "Выполнено!", "Установка выполнена успешно!")

        except PermissionError as e:
            self.error(str(e).split("]")[1])
        except FileNotFoundError as e:
            self.error(str(e).split("]")[1])

    def uninstall(self):
        try:
            file_1, file_2 = "/usr/local/bin/bginfo.bg", "/etc/xdg/autostart/bginfo.desktop"
            if os.path.isfile(file_1):
                os.remove(file_1)
                os.system("pkill root-tail")
            if os.path.isfile(file_2):
                os.remove(file_2)
            self.window_center()
            QMessageBox.information(self, "Выполнено!", "Удаление выполнено успешно!")
        except PermissionError as e:
            self.error(str(e).split("]")[1])

    def error(self, message):
        self.window_center()
        self.err = True
        QMessageBox.critical(self, "Ошибка", message, QMessageBox.Ok)


def act_uninstall():
    print("Нажата кнопка удалить")
    act = Action(action="uninstall")
    act.act()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())
