#!/usr/bin/python

import os
import subprocess
import argparse

service_name = 'sht'

python3_location = subprocess.check_output('which python3', shell=True).decode().rstrip('\r\n')
service_dir = os.path.dirname(os.path.abspath(__file__))

    
print('pip3 install')
os.system('pip3 install -r ' + service_dir + '/requirements.txt')

content = '''
[Unit]
Description=Log sht reading to influxdb
After=network.target

[Service]
ExecStart=%s %s/sht-influx.py
Restart=always
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target

''' % (
    python3_location, 
    os.path.dirname(os.path.realpath(__file__))
)

print('write service file')
with open(service_dir + '/' + service_name + '.service', 'w') as file:
    file.write(content)
    
print('enable systemd service')
os.system('systemctl enable ' + service_dir + '/' + service_name + '.service')

print('start service')
os.system('systemctl start ' + service_name)
