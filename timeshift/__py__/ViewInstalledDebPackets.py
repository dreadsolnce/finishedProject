#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Поиск установленного deb пакета в системе,
    если пакет найден, то результатом выполнения функции
    будет значение равное 0.
"""

import subprocess


def finddeb(name):
    proc = subprocess.Popen("dpkg --list | awk '{print $2}' | grep -x %s" % name,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=open("/dev/null", "w"))
    proc.communicate()
    return proc.returncode
