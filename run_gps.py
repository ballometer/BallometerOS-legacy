import ballometer
import time
import subprocess


def set_system_time(unixtime=1601116701):
    subprocess.run(['date', '-s', '@%i' % int(unixtime)],
                   stdout=subprocess.PIPE).stdout.decode('utf-8')


gps = ballometer.GPS()

time_was_set = False
while not time_was_set:
    gps.update()
    if gps.timestamp_utc is not None:
        t = time.mktime(gps.timestamp_utc)
        if t > 0:
            set_system_time(t)
            time_was_set = True

store = ballometer.Store()
        
while True:
    gps.update()
    if gps.has_fix:
        if gps.latitude is not None:
            store.save(key='gps_latitude', value=gps.latitude)

        if gps.longitude is not None:
            store.save(key='gps_longitude', value=gps.longitude)
        
        if gps.altitude_m is not None:
            store.save(key='gps_altitude', value=gps.altitude_m)

        if gps.speed_knots is not None:
            speed = gps.speed_knots * 0.514444  # m/s
            store.save(key='gps_speed', value=speed)
       
        if gps.track_angle_deg is not None:
            store.save(key='gps_heading', value=gps.track_angle_deg)

        if gps.satellites is not None:
            store.save(key='gps_satellites', value=gps.satellites)

        if gps.horizontal_dilution is not None:
            store.save(key='gps_horizontal_dilution', value=gps.horizontal_dilution)

        time.sleep(1)
    else:
        time.sleep(0.1)
