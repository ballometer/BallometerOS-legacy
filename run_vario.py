import redis
import ballometer
import json


store = ballometer.Store()
r = redis.Redis()
vario = ballometer.Vario()

p = r.pubsub(ignore_subscribe_messages=True)
p.subscribe('save:bmp_pressure')

for message in p.listen():
    data = json.loads(message['data'])
    vario.pressure = data['value']  # Pa
    unixtime = data['unixtime']  # seconds
    vario.qnh_pa = store.qnh * 1e2  # Pa
    altitude = vario.altitude  # m
    store.save(key='bmp_altitude', value=altitude, unixtime=unixtime)
