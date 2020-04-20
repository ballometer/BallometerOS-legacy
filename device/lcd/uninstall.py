import os

service_name = 'lcd'

print('stop service')
os.system('systemctl stop ' + service_name)

print('disable systemd service')
os.system('systemctl disable `pwd`/' + service_name + '.service')

print('delete service file')
os.system('rm ' + service_name + '.service')

os.remove(os.path.dirname(os.path.realpath(__file__)) + '/flight_id.json')
os.remove(os.path.dirname(os.path.realpath(__file__)) + '/nickname.json')