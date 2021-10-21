#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    Заменяет в файле строку, содержащую искомый элемент указанный в параметре запуска
    на новую строку казанную в параметрах запуска. Поиск выполняется по первым двум
    столбцам, заменяется только первое совпадение,
    если дальше будут найдены совпадения то они будут игнорироваться.
    первый параметр - файл в котором заменяем строку
    второй параметр - что ищем
    третий параметр - на что заменяем
"""

import tempfile
import os

f_tmp = tempfile.gettempdir() + "/new.tmp"


def change_string(file, what_look, what_changing):
    if not os.path.isfile(file + ".PNO.bak"):
        os.system("sudo cp -R " + file + " " + file + ".PNO.bak")
    hit_count = False  # Счетчик совпадений
    with open(f_tmp, "w") as fw:
        with open(file, "r") as fr:
            for line in fr:
                if what_look in line and hit_count is False:
                    tup = line.split()
                    try:
                        if what_look in str(tup[0]) or what_look in str(tup[1]):
                            fw.writelines(what_changing + "\n")
                            hit_count = True
                        else:
                            fw.writelines(line)
                    except IndexError:
                        pass
                else:
                    fw.writelines(line)
    os.system("sudo mv " + f_tmp + " " + file)

