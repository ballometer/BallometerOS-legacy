import os
import subprocess
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

python3_location = subprocess.check_output('which python3', shell=True).decode().strip()

service_dir = os.path.dirname(os.path.abspath(__file__))

print('pip3 install')
os.system('pip3 install -r ' + service_dir + '/requirements.txt')


print('Enable software i2c bus 3 in adafruit blinka')

file_path = '/usr/local/lib/python3.7/dist-packages/adafruit_blinka/microcontroller/bcm283x/pin.py'
fh, abs_path = mkstemp()
with fdopen(fh,'w') as new_file:
    with open(file_path) as old_file:
        for line in old_file:
            if '(1, SCL, SDA)' in line:
                line = '    (3, 24, 23), (1, SCL, SDA), (0, D1, D0),\n'
            new_file.write(line)

copymode(file_path, abs_path)
remove(file_path)
move(abs_path, file_path)


