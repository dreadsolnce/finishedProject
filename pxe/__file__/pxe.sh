#!/bin/bash

print_usage() {
    echo 'Usage:  setup.sh [ OPTION_1 ] [ OPTION_2 ]'
    echo '  [ OPTION_1 ]:'
    echo '   - network interface name (for example: eth0, eth1, enp4s0, ens3 ...)'
    echo '  [ OPTION_2 ]:'
    echo '   - full path to pxe server (for example: /usr/Eleron/Backup/PXE_Server_20210331_update6-disk001.vdi)  '
    echo -e '\033[22;31m''\n     note: Внимание путь до файла указывать в кавычках. \n''\033[0m'
    echo -e '\033[22;31m''\n     Если есть пробелы, то не использовать знак / а просто как есть пробел. \n''\033[0m'
    echo ''   
}


if [ "$1" == "" -o "$2" == "" ] ; then
	print_usage
	exit 256
elif [ "$1" != "" -o "$2" != "" ]; then
	ip -br -f link -c a | awk '{print $1}' | grep $1 > /dev/null
	if [[ $? == 0 ]]; then
		ls $2 > /dev/null
		if [[ $? == 0 ]]; then
			sudo ip link set eth1 down > /dev/null
			if [[ $? != 0 ]]; then
				echo -e '\033[22;31m'"\nОшибка остановки сетевого интерфейса $1\n"'\033[0m'
				exit 2
			fi
			switch=pxe
			ip -br -f link -c a | awk '{print $1}' | grep $switch > /dev/null	
			if [[ $? != 0 ]]; then
				sudo ip link add name $switch type bridge
				if [[ $? != 0 ]]; then
					echo -e '\033[22;31m'"\nОшибка создания порта моста\n"'\033[0m'
					exit 3
				fi	
			fi
			sudo ip link set $1 master $switch
			if [[ $? != 0 ]]; then
				echo -e '\033[22;31m'"\nОшибка создания мастер интерфейса\n"'\033[0m'
				exit 4
			fi
			ip -br -f link -c a | awk '{print $1}' | grep $switch > /dev/null	
			if [[ $? != 0 ]]; then
				sudo ip addr add 192.168.250.249/16 dev $switch brd 192.168.255.255 > /dev/null
				if [[ $? != 0 ]]; then
					echo -e '\033[22;31m'"\nОшибка присвоения ip адреса сетевому мосту\n"'\033[0m'
					exit 5
				fi
			fi
			sudo ip link set up $1 > /dev/null
			if [[ $? != 0 ]]; then
				echo -e '\033[22;31m'"\nОшибка включения сетевого интерфейса $1\n"'\033[0m'
				exit 6
			fi	
			sudo ip link set up $switch > /dev/null
			if [[ $? != 0 ]]; then
				echo -e '\033[22;31m'"\nОшибка включения сетевого моста\n"'\033[0m'
				exit 7
			fi	
			sudo qemu-system-x86_64 -name "PXE SERVER" -m 512 -hda $2 -enable-kvm -net nic,vlan=0 -net tap,vlan=0,ifname=tap0,script=/etc/qemu-ifup.PNOSKO,downscript=/etc/qemu-ifdown.PNOSKO -localtime &
			if [[ $? != 0 ]]; then
				echo -e '\033[22;31m'"\nОшибка запуска виртуальной машины qemu\n"'\033[0m'
				exit 8
			fi
		elif [[ $? != 0 ]]; then
			echo -e '\033[22;31m'"\nНе найден файл PXE сервера\n"'\033[0m'
			exit 1
		fi
	elif [[ $? != 0 ]]; then
		echo -e '\033[22;31m'"\nНет такого сетевого интерфейса\n"'\033[0m'
		exit 1
	fi
fi
	
exit 0
