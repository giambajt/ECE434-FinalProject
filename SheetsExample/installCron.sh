#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Installing crontab entery for turning off LED triggers at night
# and sending sms message when running
echo "
# Turn on logging for temperature sensor
* * * * *   root    (/home/debian/ECE434-FinalProject/SheetsExample/&& ./demo.py)
" >> /etc/crontab

#If you want to use messages at /var/log/messages
#echo "
# Turn on logging for temperature sensor with messages
#* * * * *  root (/home/debian/ECE-434FinalProject/SheetsExample && ./demo.py) 2>&1 | logger
#" >> /etc/crontab
