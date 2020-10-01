import adafruit_gps
import serial 
import time
import subprocess

def set_system_time(unixtime=1601116701):
    subprocess.run(['date', '-s', '@%i' % int(unixtime)], stdout=subprocess.PIPE).stdout.decode('utf-8')
           
if __name__ == '__main__':
    gps = adafruit_gps.GPS(serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=10), debug=False)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    gps.send_command(b"PMTK220,1000")
    time_was_set = False
    while not time_was_set:
        gps.update()
        if gps.timestamp_utc is not None:
            t = time.mktime(gps.timestamp_utc)
            if t > 0:
                set_system_time(t)
                time_was_set = True
            