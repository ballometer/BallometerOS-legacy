import ballometer
import time
import subprocess


def set_system_time(unixtime=1601116701):
    subprocess.run(['date', '-s', '@%i' % int(unixtime)],
                   stdout=subprocess.PIPE).stdout.decode('utf-8')


gps = ballometer.GPS()
store = ballometer.Store()

time_was_set = False
while not time_was_set:
    gps.update()
    if gps.timestamp_utc is not None:
        t = time.mktime(gps.timestamp_utc)
        if t > 0:
            set_system_time(t)
            time_was_set = True

while True:
    gps.update()
    if gps.has_fix:
        store.save(key='gps_latitude', value=gps.latitude)
        store.save(key='gps_longitude', value=gps.longitude)
        time.sleep(1)
