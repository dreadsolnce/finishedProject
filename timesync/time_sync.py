#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Программа настройки синхронизации времени
"""

import os
import sys
import subprocess
import shutil
import threading

# Импорт локальных модулей в зависимости от версии ОС Astra Linux
proc = subprocess.Popen("cat /etc/lsb-release | grep DISTRIB_RELEASE | awk -F= '{print $2}'",
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
out = proc.communicate()[0].decode('utf-8').split()
if out[0] == "1.4":
    version_os = "1.4"
    launch_dir = os.path.dirname(__file__)
    sys.path.append(launch_dir + "/__py__")
    err = os.system("dpkg --list | grep python3-pyqt5 >/dev/null")
    if err != 0:
        err = os.system("sudo dpkg -i " + launch_dir + "/__file__/lib* " +
                        launch_dir + "/__file__/python3-sip* " +
                        launch_dir + "/__file__/python3-pyqt5*")
        if err != 0:
            print("Ошибка установки библиотеки pyqt5!")
            exit()
    from PyQt5 import QtWidgets, QtGui, QtCore
    from PyQt5.QtWidgets import QMessageBox
    # noinspection PyUnresolvedReferences
    from main import Ui_MainWindow
    # noinspection PyUnresolvedReferences
    from debug_win import Ui_Dialog
    # noinspection PyUnresolvedReferences
    from MChangeFile import ReplaceTemplate, ReplaceTemplateOneFind
else:
    version_os = "other"
    from __py__.main import Ui_MainWindow
    from __py__.debug_win import Ui_Dialog
    from __py__.MChangeFile import ReplaceTemplate, ReplaceTemplateOneFind
    from PyQt5 import QtWidgets, QtGui, QtCore
    from PyQt5.QtWidgets import QMessageBox


file_path = sys.path[0] + "/__file__/"  # Каталог с файлами


class TIME_SYNC(QtWidgets.QMainWindow, Ui_MainWindow, threading.Thread):
    def __init__(self, path_to_img):
        super().__init__()
        self.ip_master_given = None
        self.ip_slave_given = None
        self.debug_ui = Debug_Window(None)
        self.path_to_img = path_to_img
        # инициализация основного окна
        self.ui_main = Ui_MainWindow()
        icon_tray = QtGui.QIcon()
        icon_tray.addPixmap(QtGui.QPixmap(path_to_img + "/clock.png"))
        self.setWindowIcon(icon_tray)
        self.ui_main.setupUi(self)
        self.show()
        self.act()

    def act(self):
        self.ui_main.radioButton.clicked.connect(self.clicked_main_srv)
        self.ui_main.radioButton_2.clicked.connect(self.clicked_slave_srv)
        self.ui_main.radioButton_3.clicked.connect(self.clicked_client)

        self.ui_main.checkBox.clicked.connect(self.clicked_checkbox_master)
        self.ui_main.checkBox_2.clicked.connect(self.clicked_checkbox_slave)
        self.ui_main.checkBox_3.clicked.connect(self.clicked_checkbox_interval)

        self.ui_main.pushButton_3.clicked.connect(self.clicked_test)
        self.ui_main.pushButton_2.clicked.connect(self.clicked_apply)
        self.ui_main.pushButton.clicked.connect(self.clicked_default)

    def clicked_main_srv(self):
        self.ui_main.checkBox.setDisabled(True)
        self.ui_main.checkBox.setChecked(False)

        self.ui_main.checkBox_2.setDisabled(True)
        self.ui_main.checkBox_2.setChecked(False)

        self.ui_main.checkBox_3.setDisabled(True)
        self.ui_main.checkBox_3.setChecked(False)

        self.ui_main.lineEdit.setDisabled(True)
        self.ui_main.lineEdit_2.setDisabled(True)
        self.ui_main.spinBox.setDisabled(True)

        self.ui_main.pushButton_2.setEnabled(True)
        self.ui_main.pushButton_3.setDisabled(True)

    def clicked_slave_srv(self):
        # self.ui_main.lineEdit.setEnabled(True)
        self.ui_main.checkBox.setEnabled(True)
        self.ui_main.checkBox_2.setDisabled(True)
        self.ui_main.checkBox_2.setChecked(False)
        self.ui_main.checkBox_3.setEnabled(True)
        self.ui_main.lineEdit_2.setDisabled(True)
        self.ui_main.pushButton_2.setDisabled(True)

        if self.ui_main.checkBox.isChecked() and self.ui_main.checkBox_3.isChecked():
            self.ui_main.pushButton_2.setEnabled(True)
            self.ui_main.pushButton_3.setEnabled(True)
        else:
            self.ui_main.pushButton_2.setDisabled(True)
            self.ui_main.pushButton_3.setDisabled(True)

    def clicked_client(self):
        self.ui_main.checkBox.setEnabled(True)
        self.ui_main.checkBox_2.setEnabled(True)
        self.ui_main.checkBox_3.setEnabled(True)

        if self.ui_main.checkBox.isChecked() and self.ui_main.checkBox_3.isChecked():
            self.ui_main.pushButton_2.setEnabled(True)
            self.ui_main.pushButton_3.setEnabled(True)
        else:
            self.ui_main.pushButton_2.setDisabled(True)
            self.ui_main.pushButton_3.setDisabled(True)

    def clicked_checkbox_master(self):
        if self.ui_main.checkBox.isChecked():
            self.ui_main.lineEdit.setEnabled(True)
        elif not self.ui_main.checkBox.isChecked():
            self.ui_main.lineEdit.setDisabled(True)

        if self.ui_main.checkBox.isChecked() and self.ui_main.checkBox_3.isChecked():
            self.ui_main.pushButton_2.setEnabled(True)
            self.ui_main.pushButton_3.setEnabled(True)
        else:
            self.ui_main.pushButton_2.setDisabled(True)
            self.ui_main.pushButton_3.setDisabled(True)

    def clicked_checkbox_slave(self):
        if self.ui_main.checkBox_2.isChecked():
            self.ui_main.lineEdit_2.setEnabled(True)
        elif not self.ui_main.checkBox_2.isChecked():
            self.ui_main.lineEdit_2.setDisabled(True)

        if self.ui_main.checkBox.isChecked() and self.ui_main.checkBox_3.isChecked():
            self.ui_main.pushButton_2.setEnabled(True)
            self.ui_main.pushButton_3.setEnabled(True)
        else:
            self.ui_main.pushButton_2.setDisabled(True)
            self.ui_main.pushButton_3.setDisabled(True)

    def clicked_checkbox_interval(self):
        if self.ui_main.checkBox_3.isChecked():
            self.ui_main.spinBox.setEnabled(True)
        elif not self.ui_main.checkBox_3.isChecked():
            self.ui_main.spinBox.setDisabled(True)

        if self.ui_main.checkBox.isChecked() and self.ui_main.checkBox_3.isChecked():
            self.ui_main.pushButton_2.setEnabled(True)
            self.ui_main.pushButton_3.setEnabled(True)
        else:
            self.ui_main.pushButton_2.setDisabled(True)
            self.ui_main.pushButton_3.setDisabled(True)

    def clicked_apply(self):
        if self.ui_main.radioButton.isChecked():
            response = QMessageBox.question(self, "Информация", "Главный сервер будет настроен на использование сети 192.168.0.0. "
                                                                "Для изменения данного параметра необходимо вручную изменить файл ntp.conf "
                                                                "расположенный в папке __file__.\n Настроить главный сервер синхронизации?",
                                 QMessageBox.Ok | QMessageBox.Cancel)
            if response == QMessageBox.Ok:
                self.debug_ui.plainTextEdit.insertPlainText("Ждите...")
                self.apply_master_server()
        elif self.ui_main.radioButton_2.isChecked():
            response = QMessageBox.information(self, "Информация", "Будет выполнена настройка резервного сервера!",
                                               QMessageBox.Ok | QMessageBox.Cancel)
            if response == QMessageBox.Ok:
                self.apply_slave_server()

        elif self.ui_main.radioButton_3.isChecked():
            response = QMessageBox.information(self, "Информация", "Будет выполнена настройка синхронизации времени клиента с указанными серверами",
                                               QMessageBox.Ok | QMessageBox.Cancel)
            if response == QMessageBox.Ok:
                self.apply_client_sync()

    def clicked_default(self):
        self.default_settings()

    def clicked_test(self):
        response = QMessageBox.information(self, "Информация",
                                           "Будет выполнена попытка синхронизации времени с указанными "
                                           "серверами ",
                                           QMessageBox.Ok | QMessageBox.Cancel)
        if response == QMessageBox.Ok:
            if self.ui_main.checkBox.isChecked() and \
                    str(self.ui_main.lineEdit.text().split('.')[0]) and \
                    str(self.ui_main.lineEdit.text().split('.')[1]) and \
                    str(self.ui_main.lineEdit.text().split('.')[2]) and \
                    str(self.ui_main.lineEdit.text().split('.')[3]):

                self.ip_master_given = str(int(self.ui_main.lineEdit.text().split('.')[0])) + "." + \
                     str(int(self.ui_main.lineEdit.text().split('.')[1])) + "." + \
                     str(int(self.ui_main.lineEdit.text().split('.')[2])) + "." + \
                     str(int(self.ui_main.lineEdit.text().split('.')[3]))

                self.debug_ui = Debug_Window(self.ui_main.lineEdit.text())
                self.debug_ui.show()
                #  self.debug_ui.plainTextEdit.insertPlainText("ping to " + self.ui_main.lineEdit.text() + "...Ждите")
                self.debug_ui.plainTextEdit.insertPlainText("ping to " + self.ip_master_given + "...Ждите")
                #  self.ping_to_srv(self.ui_main.lineEdit.text())
                self.ping_to_srv(self.ip_master_given)

            if self.ui_main.checkBox_2.isChecked() and \
                    str(self.ui_main.lineEdit_2.text().split('.')[0]) and \
                    str(self.ui_main.lineEdit_2.text().split('.')[1]) and \
                    str(self.ui_main.lineEdit_2.text().split('.')[2]) and \
                    str(self.ui_main.lineEdit_2.text().split('.')[3]):

                self.ip_slave_given = str(int(self.ui_main.lineEdit_2.text().split('.')[0])) + "." + \
                            str(int(self.ui_main.lineEdit_2.text().split('.')[1])) + "." + \
                            str(int(self.ui_main.lineEdit_2.text().split('.')[2])) + "." + \
                            str(int(self.ui_main.lineEdit_2.text().split('.')[3]))
                self.debug_ui.plainTextEdit.insertPlainText("\nping to " + self.ip_slave_given + "...Ждите")
                self.ping_to_srv(self.ip_slave_given)

            self.debug_ui.pushButton.setEnabled(True)

    def ping_to_srv(self, ip_srv):
        p = Ping_to_Server(ip_srv)
        p.start()
        while p.isRunning():
            QtCore.QCoreApplication.processEvents()
            QtCore.QThread.msleep(150)
        p.quit()
        if p.exit_code == 0:
            self.debug_ui.plainTextEdit.insertPlainText(
                " \nping to " + ip_srv + "...Успешно")
            self.sync_to_srv(ip_srv)
        elif p.exit_code == 1:
            self.debug_ui.plainTextEdit.insertPlainText(
                " \nping to " + ip_srv + "...Ошибка")
        else:
            QMessageBox.warning(self, "Ошибка", "Ошибка в поле адреса!")

    def sync_to_srv(self, ip_srv):
        self.debug_ui.plainTextEdit.insertPlainText("\nsync to " + ip_srv + "...Ждите")
        p = Sync_to_Server(ip_srv)
        p.start()
        while p.isRunning():
            QtCore.QCoreApplication.processEvents()
            QtCore.QThread.msleep(150)
        p.quit()
        if p.exit_code == 0:
            self.debug_ui.plainTextEdit.insertPlainText(" \nsync to " + ip_srv + "...Успешно")
        elif p.exit_code == 1:
            self.debug_ui.plainTextEdit.insertPlainText(" \nsync to " + ip_srv + "...Ошибка")

    def apply_master_server(self):
        self.debug_ui = Debug_Window("")
        self.debug_ui.show()
        self.debug_ui.plainTextEdit.insertPlainText("Ждите...")
        p_th = Apply_Master_Srv()
        p_th.start()
        while p_th.isRunning():
            QtCore.QCoreApplication.processEvents()
            QtCore.QThread.msleep(150)
        p_th.quit()
        self.debug_ui.close()
        if p_th.val_err:
            QMessageBox.information(self, "Информация", p_th.text_err)
        else:
            QMessageBox.critical(self, "Ошибка", p_th.text_err)

    def apply_slave_server(self):
        self.debug_ui = Debug_Window("")
        self.debug_ui.show()
        self.debug_ui.plainTextEdit.insertPlainText("Ждите...\n")
        #  p_th = APPLY_SLAVE_SRV(self.ui_main.lineEdit.text(), self.ui_main.spinBox.text())

        ip_master_given = str(int(self.ui_main.lineEdit.text().split('.')[0])) + "." + \
            str(int(self.ui_main.lineEdit.text().split('.')[1])) + "." + \
            str(int(self.ui_main.lineEdit.text().split('.')[2])) + "." + \
            str(int(self.ui_main.lineEdit.text().split('.')[3]))
        p_th = APPLY_SLAVE_SRV(ip_master_given, self.ui_main.spinBox.text())
        #  p_th = APPLY_SLAVE_SRV(self.ip_master, self.ui_main.spinBox.text())
        p_th.start()
        while p_th.isRunning():
            QtCore.QCoreApplication.processEvents()
            QtCore.QThread.msleep(150)
        p_th.quit()
        if p_th.val_err:
            self.debug_ui.plainTextEdit.insertPlainText("Настройка резервного сервера для синхронизации времени...Успех")
        else:
            for i in range(len(p_th.text_err)):
                self.debug_ui.plainTextEdit.insertPlainText(p_th.text_err[i])
        self.debug_ui.pushButton.setEnabled(True)

    def apply_client_sync(self):
        self.debug_ui = Debug_Window(None)
        self.debug_ui.show()
        self.debug_ui.plainTextEdit.insertPlainText("Ждите...\n")
        #  ip_master = self.ui_main.lineEdit.text()

        ip_master_given = str(int(self.ui_main.lineEdit.text().split('.')[0])) + "." + \
            str(int(self.ui_main.lineEdit.text().split('.')[1])) + "." + \
            str(int(self.ui_main.lineEdit.text().split('.')[2])) + "." + \
            str(int(self.ui_main.lineEdit.text().split('.')[3]))

        if self.ui_main.checkBox_2.isChecked():
            ip_slave_given = str(int(self.ui_main.lineEdit_2.text().split('.')[0])) + "." + \
                              str(int(self.ui_main.lineEdit_2.text().split('.')[1])) + "." + \
                              str(int(self.ui_main.lineEdit_2.text().split('.')[2])) + "." + \
                              str(int(self.ui_main.lineEdit_2.text().split('.')[3]))
        else:
            ip_slave_given = "None"
        time_interval = self.ui_main.spinBox.text()
        p_th = APPLY_CLIENT(time_interval, ip_master_given, ip_slave_given)
        p_th.start()
        while p_th.isRunning():
            QtCore.QCoreApplication.processEvents()
            QtCore.QThread.msleep(150)
        p_th.quit()
        if p_th.val_err:
            self.debug_ui.plainTextEdit.insertPlainText("Настройка клиента для синхронизации времени...Успех")
        else:
            for i in range(len(p_th.text_err)):
                self.debug_ui.plainTextEdit.insertPlainText(p_th.text_err[i])
        self.debug_ui.pushButton.setEnabled(True)

    def default_settings(self):
        self.debug_ui = Debug_Window("")
        self.debug_ui.show()
        self.debug_ui.plainTextEdit.insertPlainText("Ждите...\n")
        p_th = DEFAULT_SETTINGS()
        p_th.start()
        while p_th.isRunning():
            QtCore.QCoreApplication.processEvents()
            QtCore.QThread.msleep(150)
        p_th.quit()
        if p_th.val_err:
            self.debug_ui.plainTextEdit.insertPlainText("Сброс в настройки по умолчанию...Успех")
        else:
            for i in range(len(p_th.text_err)):
                self.debug_ui.plainTextEdit.insertPlainText(p_th.text_err[i])
        self.debug_ui.pushButton.setEnabled(True)


class Debug_Window(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, ip_master):
        super().__init__()
        self.ip_master = ip_master
        # ip_spl = str(self.ip_master).split('.')[0:4]
        # ip_join = '.'.join(ip_spl)
        self.setupUi(self)
        # self.plainTextEdit.insertPlainText("ping to " + str(ip_join) + "...Ждите")
        self.act()

    def act(self):
        self.pushButton.clicked.connect(self.clicked_close)

    def clicked_close(self):
        self.close()


class Ping_to_Server(QtCore.QThread):
    def __init__(self, ip_srv):
        super().__init__()
        self.exit_code = None
        self.ip_srv = ip_srv

    def run(self):
        process = subprocess.Popen("ping -c 2 " + self.ip_srv, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        process.communicate()
        if process.returncode != 0:
            self.exit_code = 1
        elif process.returncode == 0:
            self.exit_code = 0


class Sync_to_Server(QtCore.QThread):
    def __init__(self, ip_srv):
        super().__init__()
        self.exit_code = None
        self.ip_srv = ip_srv
        self.ntp_status = False

    def run(self):
        process = subprocess.Popen("sudo service ntp status", shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        process.communicate()
        if process.returncode == 0:
            self.ntp_status = True
            subprocess.Popen("sudo service ntp stop", shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        process = subprocess.Popen("sudo ntpdate -u " + self.ip_srv + " >/dev/null", shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out_data, err_data = process.communicate()
        if err_data:
            self.exit_code = 1
        elif not err_data:
            self.exit_code = 0
        if self.ntp_status:
            subprocess.Popen("sudo service ntp start", shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)


class Apply_Master_Srv(QtCore.QThread):
    def __init__(self):
        super().__init__()
        self.val_err = True
        self.text_err = "Успех!"

    def run(self):
        if not os.path.isfile("/etc/ntp.conf.PNOSKO.bak"):
            process = subprocess.Popen("sudo cp -R /etc/ntp.conf /etc/ntp.conf.PNOSKO.bak",
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            process.communicate()
            if process.returncode != 0:
                self.text_err = "Ошибка создания копии системного файла ntp.conf"
                self.val_err = False
        if self.val_err:
            process = subprocess.Popen("sudo service ntp stop", shell=True)
            process.communicate()
            if process.returncode != 0:
                self.text_err = "Ошибка", "Ошибка остановки службы ntp"
                self.val_err = False
        if self.val_err:
            process = subprocess.Popen("sudo cp -R " + file_path + "ntp.conf /etc/ntp.conf", shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            process.communicate()
            if process.returncode != 0:
                self.text_err = "Ошибка копирования файла ntp.conf в /etc/ntp.conf"
                self.val_err = False
        if self.val_err:
            e = None
            if version_os == "1.4":
                process = subprocess.Popen("sudo chkconfig ntp on", shell=True)
                process.communicate()
                e = process.returncode
            elif version_os == "other":
                process = subprocess.Popen("sudo systemctl enable ntp", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                process.communicate()
                e = process.returncode
            if e != 0:
                self.text_err = "Ошибка добавления службы ntp в атозагрузку"
                self.val_err = False
        if self.val_err:
            process = subprocess.Popen("sudo service ntp start", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.communicate()
            if process.returncode != 0:
                self.text_err = "Ошибка запуска службы ntp"
                self.val_err = False
        if self.val_err:
            process = subprocess.Popen("sudo cp -R " + file_path + "time_sync_primary_srv.sh /usr/local/bin/time_sync_client.sh",
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            process.communicate()
            if process.returncode != 0:
                self.text_err = "Ошибка при копировании sync_primary_srv.sh в /usr/local/bin"
                self.val_err = False
            else:
                process = subprocess.Popen("sudo chmod 777 /usr/local/bin/time_sync_client.sh", shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                process.communicate()
                if process.returncode != 0:
                    self.text_err = "Ошибка при изменении разрешений на файл /usr/local/bin/time_sync_client.sh"
                    self.val_err = False
        if self.val_err:
            shutil.copyfile(file_path + "timesync", file_path + "timesync_to_move")
            e = ReplaceTemplate(file_path + "timesync_to_move",
                                "$TIME",
                                "*/30 * * * *	root	sleep $(shuf -i 1-240 -n 1); time_sync_client.sh")
            if e.exit_code != 0:
                self.text_err = "Ошибка изменения файла timesync_to_move"
                self.val_err = False
        if self.val_err:
            process = subprocess.Popen("sudo mv " + file_path + "timesync_to_move /etc/cron.d/timesync",
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            process.communicate()
            if process.returncode != 0:
                self.text_err = "Ошибка при копировании в /etc/cron.d/timesync"
                self.val_err = False
        if self.val_err:
            process = subprocess.Popen("sudo chmod 644 /etc/cron.d/timesync", shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            process.communicate()
            if process.returncode != 0:
                self.text_err = "Ошибка при изменении разрешений на файл /etc/cron.d/timesync"
                self.val_err = False
        if self.val_err:
            process = subprocess.Popen("sudo chown root:root /etc/cron.d/timesync", shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            process.communicate()
            if process.returncode != 0:
                self.text_err = "Ошибка при изменении владельца на файл /etc/cron.d/timesync"
                self.val_err = False


class APPLY_SLAVE_SRV(QtCore.QThread):
    def __init__(self, ip_primary_srv, time_interval):
        super().__init__()
        self.ip_primary_srv = ip_primary_srv
        self.time_interval = time_interval
        self.val_err = True
        self.text_err = "Успех!"

    def run(self):
        if not os.path.isfile("/etc/ntp.conf.PNOSKO.bak"):
            process = subprocess.Popen("sudo cp -R /etc/ntp.conf /etc/ntp.conf.PNOSKO.bak",
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            process.communicate()
            if process.returncode != 0:
                self.text_err = "Ошибка создания копии системного файла ntp.conf"
                self.val_err = False
        if self.val_err:
            process = subprocess.Popen("sudo service ntp stop", shell=True)
            process.communicate()
            if process.returncode != 0:
                self.text_err = "Ошибка", "Ошибка остановки службы ntp"
                self.val_err = False
        if self.val_err:
            process = subprocess.Popen("sudo cp -R " + file_path + "ntp.conf /etc/ntp.conf", shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            process.communicate()
            if process.returncode != 0:
                self.text_err = "Ошибка копирования файла ntp.conf в /etc/ntp.conf"
                self.val_err = False
        if self.val_err:
            e = None
            if version_os == "1.4":
                process = subprocess.Popen("sudo chkconfig ntp on", shell=True)
                process.communicate()
                e = process.returncode
            elif version_os == "other":
                process = subprocess.Popen("sudo systemctl enable ntp", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                process.communicate()
                e = process.returncode
            if e != 0:
                self.text_err = "Ошибка добавления службы ntp в атозагрузку"
                self.val_err = False
        if self.val_err:
            process = subprocess.Popen("sudo service ntp start", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.communicate()
            if process.returncode != 0:
                self.text_err = "Ошибка запуска службы ntp"
                self.val_err = False
        if self.val_err:
            shutil.copyfile(file_path + "time_sync_secondary_srv.sh", file_path + "timesync_secondary_srv_to_move.sh")
            e = ReplaceTemplateOneFind(file_path + "timesync_secondary_srv_to_move.sh",
                                "primary_srv",
                                'primary_srv="' + self.ip_primary_srv + '"')
            if e.exit_code != 0:
                self.text_err = "Ошибка изменения файла timesync_secondary_srv_to_move.sh"
                self.val_err = False
        if self.val_err:
            process = subprocess.Popen("sudo mv " + file_path + "timesync_secondary_srv_to_move.sh /usr/local/bin/time_sync_client.sh",
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            process.communicate()
            if process.returncode != 0:
                self.text_err = "Ошибка при копировании в /usr/local/bin/"
                self.val_err = False
            else:
                process = subprocess.Popen("sudo chmod 777 /usr/local/bin/time_sync_client.sh", shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                process.communicate()
                if process.returncode != 0:
                    self.text_err = "Ошибка при изменении разрешений на файл /usr/local/bin/time_sync_client.sh"
                    self.val_err = False
        if self.val_err:
            shutil.copyfile(file_path + "timesync", file_path + "timesync_to_move")
            e = ReplaceTemplateOneFind(file_path + "timesync_to_move",
                                       "$TIME",
                                       "*/" + self.time_interval + " * * * *	root	sleep $(shuf -i 1-240 -n 1); time_sync_client.sh")
            if e.exit_code != 0:
                self.text_err = "Ошибка изменения файла timesync_to_move"
                self.val_err = False
        if self.val_err:
            process = subprocess.Popen("sudo mv " + file_path + "timesync_to_move /etc/cron.d/timesync",
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            process.communicate()
            if process.returncode != 0:
                self.text_err = "Ошибка при копировании в /etc/cron.d/timesync"
                self.val_err = False
        if self.val_err:
            process = subprocess.Popen("sudo chmod 644 /etc/cron.d/timesync", shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            process.communicate()
            if process.returncode != 0:
                self.text_err = "Ошибка при изменении разрешений на файл /etc/cron.d/timesync"
                self.val_err = False
        if self.val_err:
            process = subprocess.Popen("sudo chown root:root /etc/cron.d/timesync", shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            process.communicate()
            if process.returncode != 0:
                self.text_err = "Ошибка при изменении владельца на файл /etc/cron.d/timesync"
                self.val_err = False


class APPLY_CLIENT(QtCore.QThread):
    def __init__(self, time_interval, ip_master, ip_slave):
        super().__init__()
        self.time_interval = time_interval
        self.ip_master = ip_master
        self.ip_slave = ip_slave
        self.val_err = True
        self.text_err = "Успех!"
        self.e = None

    def run(self):
        process = subprocess.Popen("sudo service ntp stop", shell=True)
        process.communicate()
        if process.returncode != 0:
            self.text_err = "Ошибка", "Ошибка остановки службы ntp"
            self.val_err = False

        if self.val_err:
            if version_os == "1.4":
                process = subprocess.Popen("sudo chkconfig ntp off", shell=True)
                process.communicate()
                self.e = process.returncode
            elif version_os == "other":
                process = subprocess.Popen("sudo systemctl disable ntp", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                process.communicate()
                self.e = process.returncode
            if self.e != 0:
                self.text_err.append("Добавление службы ntp в атозагрузку...Ошибка\n")
                self.val_err = False

        if self.val_err:
            shutil.copyfile(file_path + "time_sync_client.sh", file_path + "time_sync_client_to_move.sh")
            e = ReplaceTemplateOneFind(file_path + "time_sync_client_to_move.sh",
                                       "primary_srv",
                                       'primary_srv="' + self.ip_master + '"')
            if e.exit_code == 0:
                e = ReplaceTemplateOneFind(file_path + "time_sync_client_to_move.sh",
                                           "secondary_srv",
                                           'secondary_srv="' + self.ip_slave + '"')
                if e.exit_code != 0:
                    self.text_err = "Ошибка изменения файла time_sync_client_to_move.sh"
                    self.val_err = False
            else:
                self.text_err = "Ошибка изменения файла time_sync_client_to_move.sh"
                self.val_err = False

        if self.val_err:
            process = subprocess.Popen("sudo mv " + file_path + "time_sync_client_to_move.sh /usr/local/bin/time_sync_client.sh",
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            process.communicate()
            if process.returncode != 0:
                self.text_err = "Ошибка при копировании в /usr/local/bin/"
                self.val_err = False
            else:
                process = subprocess.Popen("sudo chmod 777 /usr/local/bin/time_sync_client.sh", shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                process.communicate()
                if process.returncode != 0:
                    self.text_err = "Ошибка при изменении разрешений на файл /usr/local/bin/time_sync_client.sh"
                    self.val_err = False

        if self.val_err:
            shutil.copyfile(file_path + "timesync", file_path + "timesync_to_move")
            e = ReplaceTemplateOneFind(file_path + "timesync_to_move",
                                       "$TIME",
                                       "*/" + self.time_interval + " * * * *	root	sleep $(shuf -i 1-240 -n 1); time_sync_client.sh")
            if e.exit_code != 0:
                self.text_err = "Ошибка изменения файла timesync_to_move"
                self.val_err = False
            if self.val_err:
                process = subprocess.Popen("sudo mv " + file_path + "timesync_to_move /etc/cron.d/timesync",
                                           shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                process.communicate()
                if process.returncode != 0:
                    self.text_err = "Ошибка при копировании в /etc/cron.d/timesync"
                    self.val_err = False
            if self.val_err:
                process = subprocess.Popen("sudo chmod 644 /etc/cron.d/timesync", shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                process.communicate()
                if process.returncode != 0:
                    self.text_err = "Ошибка при изменении разрешений на файл /etc/cron.d/timesync"
                    self.val_err = False
            if self.val_err:
                process = subprocess.Popen("sudo chown root:root /etc/cron.d/timesync", shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                process.communicate()
                if process.returncode != 0:
                    self.text_err = "Ошибка при изменении владельца на файл /etc/cron.d/timesync"
                    self.val_err = False


class DEFAULT_SETTINGS(QtCore.QThread, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.val_err = True
        self.text_err = []
        self.e = None

    def run(self):
        if os.path.isfile("/etc/ntp.conf.PNOSKO.bak"):
            process = subprocess.Popen("sudo mv /etc/ntp.conf.PNOSKO.bak /etc/ntp.conf", shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            process.communicate()
            if process.returncode != 0:
                self.text_err.append("Копирование файла /etc/ntp.conf.PNOSKO.bak...Ошибка\n")
                self.val_err = False
        #  else:
        #      process = subprocess.Popen("sudo cp -R " + file_path + "ntp.conf.origin /etc/ntp.conf", shell=True,
        #                                 stdout=subprocess.PIPE,
        #                                 stderr=subprocess.PIPE)
        #      process.communicate()
        #      if process.returncode != 0:
        #          self.text_err.append("Копирование из каталога программы файла ntp.conf.origin...Ошибка\n")
        #          self.val_err = False

        if os.path.isfile("/etc/cron.d/timesync"):
            process = subprocess.Popen("sudo rm -r /etc/cron.d/timesync", shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            process.communicate()
            if process.returncode != 0:
                self.text_err.append("Удаление файла /etc/cron.d/timesync...Ошибка\n")
                self.val_err = False

        if os.path.isfile("/usr/local/bin/time_sync_client.sh"):
            process = subprocess.Popen("sudo rm -r /usr/local/bin/time_sync_client.sh", shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            process.communicate()
            if process.returncode != 0:
                self.text_err.append("Удаление файла /usr/local/bin/time_sync_client.sh...Ошибка\n")
                self.val_err = False

        if version_os == "1.4":
            process = subprocess.Popen("sudo chkconfig ntp on", shell=True)
            process.communicate()
            self.e = process.returncode
        elif version_os == "other":
            process = subprocess.Popen("sudo systemctl enable ntp", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.communicate()
            self.e = process.returncode
        if self.e != 0:
            self.text_err.append("Добавление службы ntp в атозагрузку...Ошибка\n")
            self.val_err = False

        process = subprocess.Popen("sudo service ntp start", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate()
        if process.returncode != 0:
            self.text_err.append("Запуск службы ntp...Ошибка\n")
            self.val_err = False


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    img_path = sys.path[0] + "/__img__"  # Каталог с изображениями
    t = TIME_SYNC(img_path)
    sys.exit(app.exec_())
