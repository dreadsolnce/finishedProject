#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tempfile
import shutil

# Временный файл
tmp_file = tempfile.gettempdir() + "/tmp.tmp"


# Функция записи строки в файл
class WriteStringFile:
    def __init__(self, string, file):
        print(' Функция записи строки в файл...')

        self.string = string
        self.file = file

        with open(self.file, 'w') as f:
            f.writelines(self.string)


# Функция добавления строки в файл
class AddStringFile:
    def __init__(self, string, file):
        print('Функция добавления строки в файл...')

        self.string = string
        self.file = file
        try:
            with open(self.file, 'a') as f:
                f.writelines('\n' + self.string)
                self.exit_code = 0
        except PermissionError:
            self.exit_code = 1


# Функция вывода первой строки из файла
class ReadFileOneString:
    def __init__(self, file):
        print('Функция чтения строки из файла...')

        self.file = file

        with open(self.file, 'r') as f:
            self.one_str = f.readline().rstrip('\n')

        if __name__ == '__main__':
            print("Первая строка в файле " + self.file + ': ' + self.one_str)


# Функция вывода строк из файла в список
class ReadFileStrings:
    def __init__(self, file):
        print('Функция чтения файла')

        self.file = file

        self.list_file = []
        if os.path.isfile(self.file):
            with open(self.file, 'r') as f:
                for line in f:
                    self.list_file.append(line)
        print(self.list_file)


# Функция поиска строки в файле
class FindString(object):
    def __init__(self, file, string):
        print('Функция поиска строки в файле... ')

        self.file = file
        self.string = string
        self.exit_code = -1

        self.start_func_find_string()

    def start_func_find_string(self):
        self.string = ''.join(self.string.split())

        with open(self.file, 'r') as f:
            for line in f:
                ln = ''.join(line.split())
                if ln == self.string:
                    self.exit_code = 0
        return self.exit_code


# Функция замены строки
class ChangeString:
    def __init__(self, file, old_str, new_str):
        print('Функция замены строки в файле...')

        self.file = file
        self.old_str = old_str
        self.ln_str = ''.join(old_str.split())
        self.new_str = new_str

        self.start_func_change_string()

    def start_func_change_string(self):
        with open(tmp_file, 'w') as f1:
            with open(self.file, 'r') as f:
                for line in f:
                    ln = ''.join(line.split())
                    if self.ln_str == ln:
                        f1.writelines(self.new_str + '\n')
                    else:
                        f1.writelines(line)
        shutil.move(tmp_file, self.file)


# Функция поиска шаблона (части строки) в файле
class FindTemplate(object):
    def __init__(self, file, template):
        print('Функция поиска шаблона... ')

        self.file = file
        self.template = template
        self.exit_code = -1

        self.start_func_find_template()

    def start_func_find_template(self):
        self.template = ''.join(self.template.split())

        with open(self.file, 'r') as f:
            for line in f:
                ln = ''.join(line.split())
                if self.template in ln:
                    self.exit_code = 0
        return self.exit_code


# Функция замены каждой строки которая содержит заданный шаблон
class ReplaceTemplate(object):
    def __init__(self, file, template, new_str):
        print('Функция замены каждой строки которая содержит заданный шаблон... ')

        self.file = file
        self.template = template
        self.new_str = new_str
        self.exit_code = -1

        self.start_func_replace_template()

    def start_func_replace_template(self):
        self.template = ''.join(self.template.split())
        with open(tmp_file, 'w') as f1:
            with open(self.file, 'r') as f:
                for line in f:
                    ln = ''.join(line.split())
                    if self.template in ln:
                        f1.writelines(self.new_str + '\n')
                        self.exit_code = 0
                    else:
                        f1.writelines(line)

        shutil.move(tmp_file, self.file)
        return self.exit_code


# Функция определяющая оканчивается ли файл пустой строкой
class EmptyLine(object):
    def __init__(self, file):
        self.file = file
        self.exit_code = None
        self.empty_line()

    def empty_line(self):
        with open(self.file, 'r') as f:
            last_line = f.readlines()[-1]
            ln = ''.join(last_line.split())
        if len(ln.strip(' ')) > 0:
            self.exit_code = 1  # Последняя строка не пустая
        elif len(ln.strip(' ')) == 0:
            self.exit_code = 0  # Последняя строка пустая
        return self.exit_code


# Функция удаления строки из файла, которая содержит шаблон
class DelString(object):
    def __init__(self, file, template):
        self.file = file
        self.template = template
        self.exit_code = None
        self.delete_str()

    def delete_str(self):
        self.template = ''.join(self.template.split())
        with open(tmp_file, 'w') as f1:
            with open(self.file, 'r') as f:
                i = -1
                for line in f:
                    ln = ''.join(line.split())
                    if self.template in ln:
                        pass
                    else:
                        f1.writelines(line)
        try:
            shutil.move(tmp_file, self.file)
            self.exit_code = 0
        except PermissionError as e:
            self.exit_code = 1


if __name__ == '__main__':
    pass
    # WriteStringFile('testovaya stroka 1', '/tmp/test.tmp')
    # AddStringFile('Новая строка', '/etc/apt/sources.list')
    # ReadFileOneString('/tmp/test.tmp')
    # FindString('/etc/modprobe.d/blacklist.conf', 'blacklist nouveau')
    # ChangeString('/etc/initramfs-tools/modules', 'nouveau modeset = 1', '# nouveau modeset = 1')
    # ReadFileStrings('/etc/astra_update_version')
