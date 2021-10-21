#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Поиск сетевых интерфейсов в системе.
"""

import subprocess


def find_ethernet():
    list_out = []
    proc = subprocess.Popen("ip -o link show | awk '{print $2}' | awk -F: '{print $1}'",
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=open("/dev/null", "w"))
    s = proc.stdout.readline()
    while s:
        list_out.append(s.decode('utf-8'))
        s = proc.stdout.readline()

    return list_out


if __name__ == "__main__":
    find_ethernet()
