#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Скрипт запуска PXE сервера.
"""

import os
import sys
import subprocess
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox


def start_pxe(*args):
    # Наличие сетевого интерфейса
    process = subprocess.Popen("ip -br -f link -c a | awk '{print $1}' | grep " + args[0], shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    _, err = process.communicate()
    if process.returncode != 0:
        msg_err("Не найден сетевой интерфейс")
        exit(255)

    # Проверка наличия файла PXE сервера
    if not os.path.isfile(args[1]):
        msg_err(
            "Ошибка не найден файл PXE сервера\n Если есть пробелы в названии, то необходимо экранировать кавычками")
        exit(255)

    # Выключаем сетевой интерфейс
    process = subprocess.Popen("sudo ip link set " + args[0] + " down", shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    _, err = process.communicate()
    if process.returncode != 0:
        msg_err("Ошибка остановки сетевого интерфейса")
        exit(255)

    # Проверка наличия сетевого моста
    switch = "pxe"
    process = subprocess.Popen("sudo ip -br -f link -c a | awk '{print $1}' | grep " + switch, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    _, err = process.communicate()
    if process.returncode != 0:
        # Создание сетевого моста
        process = subprocess.Popen("sudo ip link add name " + switch + " type bridge", shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        _, err = process.communicate()
        if process.returncode != 0:
            msg_err("Ошибка создания сетевого моста")
            exit(255)

    # Создание мастер интерфейса
    process = subprocess.Popen("sudo ip link set " + args[0] + " master " + switch, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    _, err = process.communicate()
    if process.returncode != 0:
        msg_err("Ошибка создания мастер интерфейса")
        exit(255)

    # ip адрес сетевому мосту: 192.168.250.249/16
    process = subprocess.Popen("sudo ip addr show " + switch + " | grep 192.168.250.249", shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    _, err = process.communicate()
    if process.returncode != 0:
        process = subprocess.Popen("sudo ip addr add 192.168.250.249/16 dev " + switch + " brd 192.168.255.255",
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        _, err = process.communicate()
        if process.returncode != 0:
            msg_err("Ошибка присвоения ip адреса сетевому мосту")
            exit(255)

    # Включение сетевых интерфейсов
    process = subprocess.Popen("sudo ip link set up " + args[0], shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    _, err = process.communicate()
    if process.returncode != 0:
        msg_err("Ошибка включения сетевого интерфейса")
        exit(255)

    process = subprocess.Popen("sudo ip link set up " + switch, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    _, err = process.communicate()
    if process.returncode != 0:
        msg_err("Ошибка включения сетевого моста")
        exit(255)

    # Запуск PXE сервера
    process = subprocess.Popen("sudo qemu-system-x86_64 -name 'PXE SERVER' -m 512 -hda '" + args[1] +
                               "' -enable-kvm -net nic,vlan=0 -net tap,vlan=0,ifname=tap0,script=/etc/qemu-ifup.PNOSKO,"
                               "downscript=/etc/qemu-ifdown.PNOSKO -localtime &",
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    _, err = process.communicate()
    if process.returncode != 0:
        msg_err("Ошибка запуска PXE сервера")
        exit(255)

    exit(0)


def msg_err(text):  # Критическое сообщение
    msg = QMessageBox()
    msg.setWindowTitle("Ошибка")
    msg.setText("%s" % text)
    msg.setIcon(QMessageBox.Critical)
    msg.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    if len(sys.argv) > 2:
        start_pxe(sys.argv[1], sys.argv[2])
    else:
        print("\n"
              "            Usage:  setup.sh [ OPTION_1 ] [ OPTION_2 ]\n"
              "                [ OPTION_1 ]:\n"
              "                  - network interface name (for example: eth0, eth1, enp4s0, ens3 ...)\n"
              "                [ OPTION_2 ]:\n"
              "                  - full path to pxe server (for example: \"/usr/Eleron/Backup/PXE Server "
              "20210331 update6 disk001.vdi\")\n"
              "                  note: Внимание путь до файла указывать в кавычках.\n"
              "                  Если есть пробелы, то не использовать знак \ а просто как есть пробел.\n"
              "        ")
        # start_pxe("enp5s0", "/home")
