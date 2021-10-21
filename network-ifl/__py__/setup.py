#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import threading

from __py__.TwoWindowInstallUninstall import *
from __py__.MainWindow import *
from __py__.ThreeWindowLocalRemote import *
from __py__.DebugLogInstallLocal import *
from __py__.RemotwDataWindow import *
from __py__.ViewInstalledDebPackets import finddeb

from time import sleep
import subprocess

from PyQt5.QtWidgets import QMessageBox

# Установка программы в локальном режиме (в отдельном потоке)
class InstallTimeShift(QtCore.QThread):
    #global new_log
    new_log = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int)
    def __init__(self):
        QtCore.QThread.__init__(self)
        #self.command = command

    def run(self):
        tar_gz_arch = dis_path + "/packages.tar.gz"
        process = subprocess.Popen("tar xvzf %s" % tar_gz_arch, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        self.string_execution = " "
        i = 0
        self.exit_code = 0
        while self.string_execution:
            self.string_execution = process.stdout.readline()
            self.new_log.emit(str(self.string_execution.decode('utf-8', 'ignore')))
            self.progress.emit(i)
            sleep(0.01)
            ui_debug.plainTextEdit.moveCursor(QtGui.QTextCursor.EndOfBlock)
            ui_debug.progressBar.setValue(i)
            i += 1
        process.communicate()
        self.exit_code = self.exit_code + process.returncode
        deb_pack = sorted((os.listdir("package")))

        for pack in deb_pack:
            process = subprocess.Popen("sudo dpkg -i package/%s" % pack, shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            self.string_execution = " "
            while self.string_execution:
                self.string_execution = process.stdout.readline()
                self.new_log.emit(str(self.string_execution.decode('utf-8', 'ignore')))
                self.progress.emit(i)
                sleep(0.01)
                ui_debug.plainTextEdit.moveCursor(QtGui.QTextCursor.EndOfBlock)
                ui_debug.progressBar.setValue(i)
                i += 1
            process.communicate()
            self.exit_code = self.exit_code + process.returncode
        self.progress.emit(100)
        if self.exit_code == 0:
            self.new_log.emit("ВЫПОЛНЕНО УСПЕШНО!")
        elif self.exit_code != 0:
            self.new_log.emit("ОШИБКА!")
        os.system("rm -rf package")

# Удаление программы в локальном режиме (в отдельном потоке)
class UninstallTimeShift(QtCore.QThread):
    new_log = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int)

    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        process = subprocess.Popen("sudo dpkg --purge timeshift",
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        self.string_execution = " "
        i = 0
        while self.string_execution:
            self.string_execution = process.stdout.readline()
            self.new_log.emit(str(self.string_execution.decode('utf-8', 'ignore')))
            self.progress.emit(i)
            sleep(0.01)
            ui_debug.plainTextEdit.moveCursor(QtGui.QTextCursor.EndOfBlock)
            ui_debug.progressBar.setValue(i)
            i += 1
        process.communicate()
        self.exit_code = process.returncode
        self.progress.emit(100)
        if self.exit_code == 0:
            self.new_log.emit("ВЫПОЛНЕНО УСПЕШНО!")
        elif self.exit_code != 0:
            self.new_log.emit("ОШИБКА!")

# Установка программы в удаленном режиме (в отдельном потоке)
class InstallTimeShiftRemote(QtCore.QThread):
    new_log = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int)

    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        import paramiko
        try:
            self.exit_code_err = 0
            cli = paramiko.client.SSHClient()
            cli.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
            #cli.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))  ###
            cli.connect(hostname=addr, username=name_user, password=password_ssh, port=22)
            i = 0
            # Копируем дистриб с программой на удаленный компьютер
            ui_debug.progressBar.setValue(i)
            sftp = cli.open_sftp()
            self.new_log.emit("Идет копирование...\n")
            sftp.put(dis_path + "/packages.tar.gz", "/tmp/packages.tar.gz")
            i += 1
            self.progress.emit(i)
            self.new_log.emit("Копирование завершено\n")
            ui_debug.progressBar.setValue(i)
            sleep(1)
            sftp.close()
            # Разархивируем каталог с программой
            self.new_log.emit("Разархивируем архив...\n")
            stdin, stdout, stderr = cli.exec_command("tar xvzf /tmp/packages.tar.gz -C /tmp/", get_pty=True)
            i += 1
            for line in iter(stdout.readline, ""):
                print(line, end="")
                self.new_log.emit(line)
                self.progress.emit(i)
                sleep(0.01)
                ui_debug.plainTextEdit.moveCursor(QtGui.QTextCursor.EndOfBlock)
                ui_debug.progressBar.setValue(i)
                i += 1
            self.exit_code_err = stdout.channel.recv_exit_status() + self.exit_code_err
            # Устанавливаем разархивированые пакеты
            stdin, stdout, stderr = cli.exec_command("sudo dpkg -i /tmp/package/*", get_pty=True)
            i += 1
            for line in iter(stdout.readline, ""):
                print(line, end="")
                self.new_log.emit(line)
                self.progress.emit(i)
                sleep(0.01)
                ui_debug.plainTextEdit.moveCursor(QtGui.QTextCursor.EndOfBlock)
                ui_debug.progressBar.setValue(i)
                i += 1
            #print ("Ошибка = " + str(stderr))
            self.exit_code_err = stdout.channel.recv_exit_status() + self.exit_code_err
            # Удаляем временные файлы
            stdin, stdout, stderr = cli.exec_command("sudo rm -rf /tmp/package*", get_pty=True)
            i += 1
            for line in iter(stdout.readline, ""):
                print(line, end="")
                self.new_log.emit(line)
                self.progress.emit(i)
                sleep(0.01)
                ui_debug.plainTextEdit.moveCursor(QtGui.QTextCursor.EndOfBlock)
                ui_debug.progressBar.setValue(i)
                i += 1
            self.exit_code_err = stdout.channel.recv_exit_status() + self.exit_code_err
            cli.close()
            self.progress.emit(100)
            if self.exit_code_err != 0:
                self.new_log.emit("Завершено c ошибкой...\n")
            else:
                self.new_log.emit("Завершено успешно...\n")
        except paramiko.ssh_exception.AuthenticationException:
            msgbox_critical("Ошибка аутентификации!")
            DebugWindow.close()
            ThreeWindow.show()
        except paramiko.ssh_exception.SSHException:
            msgbox_critical("Подключение по SSH на удаленном компьютере заблокировано!")
            DebugWindow.close()
        except paramiko.ssh_exception.NoValidConnectionsError:
            msgbox_critical("Подключение по SSH на удаленном компьютере заблокировано!")
        except OSError as err:
            msgbox_critical("Ошибка %s" % err)
            DebugWindow.close()
            ThreeWindow.show()
        except FileNotFoundError as err:
            #msgbox_critical("Дистрибутив с программой не найден!")
            msgbox_critical("Не найден файл %s" % err)
            DebugWindow.close()
        except Exception:
            msgbox_critical("Неизвестная ошибка!")
        finally:
            thread.quit()

class UninstallTimeShiftRemote(QtCore.QThread):
    new_log = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int)

    def __init__(self):
        QtCore.QThread.__init__(self)
    def run(self):
        import paramiko
        try:
            self.exit_code_err = 0
            cli = paramiko.client.SSHClient()
            cli.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
            #cli.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))  ###
            cli.connect(hostname=addr, username=name_user, password=password_ssh, port=22)
            i = 0
            ui_debug.progressBar.setValue(i)
            # Удадяем пакет timeshift
            stdin, stdout, stderr = cli.exec_command("sudo dpkg --purge timeshift", get_pty=True)
            i += 1
            for line in iter(stdout.readline, ""):
                print(line, end="")
                self.new_log.emit(line)
                self.progress.emit(i)
                sleep(0.01)
                ui_debug.plainTextEdit.moveCursor(QtGui.QTextCursor.EndOfBlock)
                ui_debug.progressBar.setValue(i)
                i += 1
            self.exit_code_err = stdout.channel.recv_exit_status() + self.exit_code_err
            cli.close()
            self.progress.emit(100)
            if self.exit_code_err != 0:
                self.new_log.emit("Завершено c ошибкой...\n")
            else:
                self.new_log.emit("Завершено успешно...\n")


        except paramiko.ssh_exception.AuthenticationException:
            msgbox_critical("Ошибка аутентификации!")
            DebugWindow.close()
            ThreeWindow.show()
        except paramiko.ssh_exception.SSHException:
            msgbox_critical("Подключение по SSH на удаленном компьютере заблокировано!")
            DebugWindow.close()
        except paramiko.ssh_exception.NoValidConnectionsError:
            msgbox_critical("Подключение по SSH на удаленном компьютере заблокировано!")
        except OSError as err:
            msgbox_critical("Ошибка %s" % err)
            DebugWindow.close()
            ThreeWindow.show()
        except FileNotFoundError as err:
            # msgbox_critical("Дистрибутив с программой не найден!")
            msgbox_critical("Не найден файл %s" % err)
            DebugWindow.close()
        except Exception:
            msgbox_critical("Неизвестная ошибка!")
        finally:
            thread.quit()

class InstallParamiko(QtCore.QThread):
    new_log = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(int)
    def run(self) :
        self.exit_code = 0
        i = 0
        tar_gz_arch = dis_path + "/paramiko.tar.gz"
        process = subprocess.Popen("tar xvzf %s" % tar_gz_arch, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        # self.string_execution = " "
        self.string_execution = process.stdout.readline()
        while self.string_execution:
            self.string_execution = process.stdout.readline()
            self.new_log.emit(str(self.string_execution.decode('utf-8', 'ignore')))
            self.progress.emit(i)
            sleep(0.01)
            ui_debug.plainTextEdit.moveCursor(QtGui.QTextCursor.EndOfBlock)
            ui_debug.progressBar.setValue(i)
            i += 1
        process.communicate()
        self.exit_code = self.exit_code + process.returncode

        process = subprocess.Popen("sudo dpkg -i paramiko/*", shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        self.string_execution = process.stdout.readline()
        while self.string_execution:
            self.string_execution = process.stdout.readline()
            self.new_log.emit(str(self.string_execution.decode('utf-8', 'ignore')))
            self.progress.emit(i)
            sleep(0.01)
            ui_debug.plainTextEdit.moveCursor(QtGui.QTextCursor.EndOfBlock)
            ui_debug.progressBar.setValue(i)
            i += 1
        process.communicate()
        self.exit_code = self.exit_code + process.returncode
        self.progress.emit(100)
        os.system("rm -rf package")

def clicked_pushButton_main_window():
    # проверить версию ОС
    number_os, number_update = version_os()
    if number_os == "1.6" and number_update in ["0", "6"]:
        # Поддерживаемая ОС
        print("Поддерживаемая ОС")
        MainWindow.close()
        #TwoWindowInstallUninstall()
        ThreeWindowLocalRemote()
    else:
        print("Не поддерживаемая ОС")
        msgbox_critical("Установленная версия ОС не поддерживается")

def clicked_pushButton_two_window():
    global thread, paramiko_thread
    TwoWindow.close()
    DebugWindowInstallLocal()
    if type_of_install == "local":
        if ui_two.comboBox.currentIndex() == 1:
            thread = InstallTimeShift()
        elif ui_two.comboBox.currentIndex() == 2:
            thread = UninstallTimeShift()
        thread.new_log.connect(ui_debug.plainTextEdit.insertPlainText)
        thread.progress.connect(ui_debug.progressBar.setValue)
        thread.start()
    elif type_of_install == "remote":
        if finddeb("python3-paramiko") != 0:
            DebugWindowInstallLocal()
            ui_debug.plainTextEdit.appendPlainText("Установка модуля PARAMIKO на локальную машину...\n")
            run = InstallParamiko()
            run.new_log.connect(ui_debug.plainTextEdit.insertPlainText)
            run.progress.connect(ui_debug.progressBar.setValue)
            run.start()
            while run.isRunning():
                QtCore.QCoreApplication.processEvents()
                QtCore.QThread.msleep(150)
            if run.exit_code == 0:
                DebugWindow.update()
                DebugWindow.close()
                run.quit()
                DebugWindowInstallLocal()
                if ui_two.comboBox.currentIndex() == 1:
                    thread = InstallTimeShiftRemote()
                elif ui_two.comboBox.currentIndex() == 2:
                    thread = UninstallTimeShiftRemote()
                thread.new_log.connect(ui_debug.plainTextEdit.insertPlainText)
                thread.progress.connect(ui_debug.progressBar.setValue)
                thread.start()
            elif run.exit_code != 0:
                ui_debug.plainTextEdit.appendPlainText("Ошибка при установке дополнительных библиотек...")
                DebugWindow.update()
                run.quit()
        elif finddeb("python3-paramiko") == 0:
            #DebugWindowInstallLocal()
            if ui_two.comboBox.currentIndex() == 1:
                thread = InstallTimeShiftRemote()
            elif ui_two.comboBox.currentIndex() == 2:
                thread = UninstallTimeShiftRemote()
            thread.new_log.connect(ui_debug.plainTextEdit.insertPlainText)
            thread.progress.connect(ui_debug.progressBar.setValue)
            thread.start()

def clicked_pushButton_three_window():
    global type_of_install
    ThreeWindow.close()
    if ui_three.checkBox_3.isChecked() == True:
        type_of_install = "local"
        TwoWindowInstallUninstall()
    elif ui_three.checkBox_4.isChecked() == True:
        type_of_install = "remote"
        RemoteDataWindow()

# Нажата кнопка применить в окне для ввода данных для удаленного подключения
def clicked_pushButton_remote_window():
    global name_user, password_ssh, addr, err
    name_user = ui_dataremote.lineEdit.text()
    password_ssh = ui_dataremote.lineEdit_2.text()
    addr = ui_dataremote.lineEdit_3.text()
    DataForRemoteWindow.close()
    TwoWindowInstallUninstall()

# Определение версии операционной системы
def version_os():
    # Номер ОС в виде 1.6
    run_command = subprocess.Popen("cat /etc/lsb-release | grep DISTRIB_RELEASE | awk -F= '{print $2}'", shell=True,
                                    stdout=subprocess.PIPE)
    number_os = run_command.communicate()[0].decode('utf-8').strip()
    # Номер обновления в виде цифры 0 или 6
    if not os.path.exists("/etc/astra_update_version"):
        number_update = "0"
    else:
        run_command = subprocess.Popen("cat /etc/astra_update_version | grep Update | awk '{print $2}'", shell=True,
                                        stdout=subprocess.PIPE)
        number_update = run_command.communicate()[0].decode('utf-8').strip()
    print("Версия ОС: " + number_os + ". Версия Update: " + number_update)
    return (number_os, number_update)

# Критическое сообщение о несовместимости версии
def msgbox_critical(text):
    global msg, exit_code_msgbox
    msg = QMessageBox()
    msg.setWindowTitle("Ошибка")
    msg.setText("%s" % text)
    msg.setIcon(QMessageBox.Critical)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(img_path + "/timeshift.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    msg.setWindowIcon(icon)
    msg.exec_()

# Второе окно программы
def TwoWindowInstallUninstall():
    global TwoWindow, ui_two
    TwoWindow = QtWidgets.QMainWindow()
    ui_two = Ui_TwoWindow()
    ui_two.setupUi(TwoWindow)
    TwoWindow.show()
    # выполняемые действия при нажатии кнопок далее или отмена
    ui_two.pushButton.clicked.connect(clicked_pushButton_two_window)
    ui_two.pushButton_2.clicked.connect(lambda: (TwoWindow.close(), ThreeWindow.show()))

# Третье окно программы (во время выпонения оно появляется вторым)
def ThreeWindowLocalRemote():
    global ThreeWindow, ui_three
    ThreeWindow = QtWidgets.QMainWindow()
    ui_three = Ui_ThreeWindow()
    ui_three.setupUi(ThreeWindow)
    ThreeWindow.show()
    #ui_three.pushButton_2.clicked.connect(lambda: (ThreeWindow.close(), TwoWindow.show()))

    ui_three.pushButton.clicked.connect(clicked_pushButton_three_window)
    ui_three.pushButton_2.clicked.connect(lambda: (ThreeWindow.close(), MainWindow.show()))

# Четвертое окно
def DebugWindowInstallLocal():
    global DebugWindow, ui_debug
    DebugWindow = QtWidgets.QMainWindow()
    #DebugWindow = QtWidgets.QDialog()
    ui_debug = Ui_DebugWindow()
    ui_debug.setupUi(DebugWindow)
    DebugWindow.show()
    ui_debug.pushButton.clicked.connect(lambda: DebugWindow.close())

# Окно ввода данных для удаленного подключения
def RemoteDataWindow():
    global DataForRemoteWindow, ui_dataremote
    DataForRemoteWindow = QtWidgets.QWidget()
    ui_dataremote = Ui_DataForRemote()
    ui_dataremote.setupUi(DataForRemoteWindow)
    DataForRemoteWindow.show()
    ui_dataremote.pushButton.clicked.connect(clicked_pushButton_remote_window)
    ui_dataremote.pushButton_2.clicked.connect(lambda: (DataForRemoteWindow.close(), ThreeWindow.show()))

def MyEnvironment(path_module):
    global img_path, dis_path
    if path_module == "main_module":
        img_path = sys.path[0] + "/__img__"  # Каталог с изображениями
        dis_path = sys.path[0] + "/__dis__"  # Каталог с дистрибутивом
    else:
        img_path = sys.path[0].rpartition('__img__')[0]  # Каталог с изображениями
        dis_path = sys.path[0].rpartition('__dis__')[0]  # Каталог с дистрибутивом
    # = sys.path[0]  # .rpartition('__py__')[0] # Каталог запуска программы
    #path_py = path_prog + "/__py__"  # Каталог с программами pyton
    #sys.path = [path_py] + sys.path

if __name__ == "__main__":
    MyEnvironment("main_module")  # Запущен как главная программа
    app = QtWidgets.QApplication(sys.argv)
    # Первое окно программы
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    # выполняемые действия при нажатии кнопок далее или отмена
    ui.pushButton.clicked.connect(clicked_pushButton_main_window)
    ui.pushButton_2.clicked.connect(MainWindow.close)
    MainWindow.show()
    sys.exit(app.exec_())
else:
    MyEnvironment("dependent_module")  # запущен как зависимый модуль

