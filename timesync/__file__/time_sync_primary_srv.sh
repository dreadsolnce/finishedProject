#!/bin/bash

sudo service ntp status &>/dev/null
if [[ $? != 0 ]];then sudo service ntp start &>/dev/null; fi

exit 0
