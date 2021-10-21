#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Программа проверки доступа к хочту по ssh
        Входные данные:
        - ip дресс удаленного хоста
        - пароль суперпользователя
        - путь к файлу с результатом проверки
"""

import paramiko
import threading


# noinspection PyBroadException
class AccessScanner(threading.Thread):
    def __init__(self, ip="127.0.0.1", password="12345678", user_name="root"):
        super().__init__()
        self.ip = ip
        self.password = password
        self.user_name = user_name

    def get_access(self):
        cli = paramiko.client.SSHClient()
        cli.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        try:
            cli.connect(hostname=self.ip, username=self.user_name, password=self.password, port=22)
        except paramiko.ssh_exception.AuthenticationException:
            return 1
        except paramiko.ssh_exception.SSHException:
            return 2
        except paramiko.ssh_exception.NoValidConnectionsError:
            return 3
        except Exception:
            return 4
        else:
            return 0

    def get_name(self):
        cli = paramiko.client.SSHClient()
        cli.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        cli.connect(hostname=self.ip, username=self.user_name, password=self.password, port=22)
        (stdin, stdout, stderr) = cli.exec_command("hostname")
        result = stdout.read()
        cli.close()
        return ' '.join(result.decode('utf-8').split())


if __name__ == "__main__":
    a = AccessScanner("192.168.100.3", "1234567")
    a.get_access()
