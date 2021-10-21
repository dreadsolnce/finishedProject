#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Программа сканирования сети
    Сканирует только одну подсеть
    Сканирование выполняется одновременно по всему диапазону
    Входные данные:
        - начальный адрес сканирования
        - конечный адрес сканирования
        - путь к файлу с результатом сканирования
"""

import socket
import os
import threading


class RunNetworkScanner(threading.Thread):
    def __init__(self, ip="127.0.0.1", f_list="/tmp/list.txt"):
        super(RunNetworkScanner, self).__init__()
        self.ip = ip
        self.f_list = f_list

    def run(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = soc.connect_ex((self.ip, 135))
            if result != 111:
                #  print("Компьютер с ip " + self.ip + " не пингуется\n")
                pass
            else:
                pass
                #  print("Компьютер с ip " + self.ip + " пингуется\n")
                with open(self.f_list, 'a') as f:
                    f.write(self.ip + "\n")
        finally:
            soc.close()


class NetworkScanner(RunNetworkScanner):
    def __init__(self, start_ip="127.0.0.1", end_ip="127.0.0.1", f_list="/tmp/list.txt"):
        super(NetworkScanner, self).__init__()
        self.start_ip = start_ip
        self.end_ip = end_ip
        self.f_list = f_list

    def start(self):
        start_ip_spl = self.start_ip.split('.')[3]
        finish_ip_spl = self.end_ip.split('.')[3]
        if os.path.exists(self.f_list):
            os.remove(self.f_list)
        for i in range(int(start_ip_spl), int(finish_ip_spl) + 1):
            ip = self.start_ip.split(".")[0] + \
                 "." + self.start_ip.split(".")[1] + \
                 "." + self.start_ip.split(".")[2] + \
                 "." + str(i)
            r = RunNetworkScanner(ip, self.f_list)
            r.start()


if __name__ == "__main__":
    s = NetworkScanner("192.168.100.1", "192.168.100.2", "/home/kvl/PycharmProjects/currentProject/__file__/list.txt")
    s.start()
