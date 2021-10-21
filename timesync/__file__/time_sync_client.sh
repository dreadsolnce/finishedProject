#!/bin/bash
primary_srv="192.168.111.11"
secondary_srv="None"

sudo service ntp status &>/dev/null
if [[ $? == 0 ]];then sudo service ntp stop &>/dev/null; fi

ping -c 1 ${primary_srv} >/dev/null
if [[ $? == 0 ]];then sudo ntpdate -u ${primary_srv} &>/dev/null; exit 0; fi

if [[ ${secondary_srv} != "None" ]]; then
	ping -c 1 ${secondary_srv} >/dev/null
	if [[ $? == 0 ]];then sudo ntpdate -u ${secondary_srv} &>/dev/null; exit 0; fi
	exit 1
fi
