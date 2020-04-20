import os
import subprocess
import json

service_name = 'lcd'

python3_location = subprocess.check_output('which python3', shell=True).decode().strip()
directory = os.path.dirname(os.path.realpath(__file__))

with open(directory + '/nickname.json', 'w') as f:
    json.dump({'nickname': ''}, f)
    
with open(directory + '/flight_id.json', 'w') as f:
    json.dump({'flight_id': 0, 'recording': False}, f)

content = '''
[Unit]
Description=service for running the LCD 

[Service]
ExecStart=%s %s/lcd.py
Restart=always
TimeoutStopSec=30
WorkingDirectory=%s

[Install]
WantedBy=basic.target

''' % (python3_location, directory, directory)

print('write service file')
with open(service_name + '.service', 'w') as file:
    file.write(content)
    
print('enable systemd service')
os.system('systemctl enable `pwd`/' + service_name + '.service')

print('start service')
os.system('systemctl start ' + service_name)
