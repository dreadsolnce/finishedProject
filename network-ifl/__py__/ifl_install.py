#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""

"""

import paramiko
import threading
import sys
import pexpect
import time


class RunCopyStartIfl(threading.Thread):
    def __init__(self, ip="127.0.0.1", password="12345678", user_name="root", file="/tmp/test.txt"):
        super().__init__()
        self.ip = ip
        self.password = password
        self.user_name = user_name
        self.file = file

    def run(self):
        err = 0
        cli = paramiko.client.SSHClient()
        cli.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        cli.connect(hostname=self.ip, username=self.user_name, password=self.password, port=22)

        sftp = cli.open_sftp()
        sftp.put(self.file, "/tmp/ImageForLinux.tar.gz")
        stdin, stdout, stderr = cli.exec_command("tar xvzf /tmp/ImageForLinux.tar.gz -C /tmp/", get_pty=True)
        err = stdout.channel.recv_exit_status() + err
        stdin, stdout, stderr = cli.exec_command("if [ -f /lib/ld-linux.so.2 ]; "
                                                 "then sleep 1 ; else sudo ln -s /tmp/ImageForLinux/lib/ld-2.24.so "
                                                 "/lib/ld-linux.so.2;fi",
                                                 get_pty=True)
        err = stdout.channel.recv_exit_status() + err
        # cli.close()
        if err == 0:
            try:
                command = 'ssh -o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking=no" ' + \
                          self.user_name + '@' + \
                          self.ip + \
                          ' LD_LIBRARY_PATH=/tmp/ImageForLinux/lib/ /tmp/ImageForLinux/imagel'
                ssh_tunnel = pexpect.spawn(command)
                ssh_tunnel.expect('password:')
                time.sleep(0.1)
                ssh_tunnel.sendline(self.password.encode('utf-8'))
                ssh_tunnel.expect(pexpect.EOF)
                cli.exec_command("rm -rf /tmp/ImageForLinux*", get_pty=True)
                cli.close()
            except Exception as e:
                print(e)
        else:
            print("Ошибка!")


class IflNetworkInstall(RunCopyStartIfl):
    def __init__(self, ip, password, user_name, file):
        super().__init__()
        self.ip = ip
        self.password = password
        self.user_name = user_name
        self.file = file

    def start(self):
        rc = RunCopyStartIfl(self.ip, self.password, self.user_name, self.file)
        rc.start()


def myenvironment(run_type):
    global file_path
    if run_type == "main":
        file_path = sys.path[0].rpartition("__py__")[0] + "__file__"


if __name__ == "__main__":
    global file_path
    myenvironment("main")  # Запущен как главная программа
    ini = IflNetworkInstall(ip="192.168.100.2", password="12345678", file=file_path + "/ImageForLinux.tar.gz")
    ini.start()
