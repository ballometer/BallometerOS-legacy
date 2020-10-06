import redis
import ballometer
import json


store = ballometer.Store()
r = redis.Redis()

p = r.pubsub(ignore_subscribe_messages=True)
p.subscribe('save:bmp_pressure')

for message in p.listen():
    data = json.loads(message['data'])
    pressure = data['value']  # Pa
    unixtime = data['unixtime']  # seconds
    qnh_pa = store.qnh * 1e2  # Pa
    altitude = 44330.0 * (1.0 - (pressure / qnh_pa) ** 0.1903)  # m
    store.save(key='bmp_altitude', value=altitude, unixtime=unixtime)
