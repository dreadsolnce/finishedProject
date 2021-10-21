#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Поиск установленного deb пакета в системе,
    если пакет найден, то результатом выполнения функции
    будет иметь значение равное 0.
"""

import subprocess
import threading


class DebInstall(threading.Thread):
    def __init__(self, *args):
        super().__init__()
        self.args = args
        self.st = None
        self.err_proc = None

    def run(self):
        for deb in self.args:

            proc = subprocess.Popen("sudo dpkg -i %s" % deb, shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            while self.st:
                self.st = proc.stdout.readline()
            proc.communicate()
            self.err_proc = proc.returncode


def find_deb(*args):
    err = 0
    for deb in args:
        proc = subprocess.Popen("dpkg --list | awk '{print $2}' | fgrep -x %s" % deb,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=open("/dev/null", "w"))
        proc.communicate()
        err = err + proc.returncode
    return err


if __name__ == "__main__":
    find_deb('python3-paramiko')
