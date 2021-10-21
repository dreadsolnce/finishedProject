#!/bin/bash
primary_srv="192.168.111.31"

ping -c 1 ${primary_srv} >/dev/null
if [[ $? == 0 ]];then 
    sudo service ntp status &>/dev/null
    if [[ $? == 0 ]];then sudo service ntp stop &>/dev/null; fi
    sudo ntpdate -u ${primary_srv} &>/dev/null
    sudo service ntp start;
    exit 0
fi

exit 1