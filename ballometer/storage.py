import influxdb
import redis
import time


class Store:
    def __init__(self):
        self._db_name = 'ballometer'
        self._influx = influxdb.InfluxDBClient()
        if self._influx.switch_database(self._db_name) is None:
            self._influx.create_database(self._db_name)
        self._redis = redis.Redis()

    def save(self, key='key-name', value=1.0, unixtime=None):
        if unixtime is None:
            unixtime = time.time()

        if unixtime < 1601116701:
            # The system time is not synchronized yet
            # and is probably still at the default value
            # in year 1970. Skip writing to influxdb.
            return

        if not self.get_volatile_float('recording'):
            # Recording has not been turned on (yet)
            # by the user. Skip writing to influxdb.
            return

        self._influx.write_points([
            {
                'measurement': key,
                'fields': {
                    'value': float(value)
                },
                'time': unixtime,
                'tags': {
                    'flight_id': str(int(self.get_volatile_float('flight_id')))
                }
            }
        ])

    def get_volatile_float(self, key='key-name'):
        value = self._redis.get(key)
        if value is None:
            return 0.0
        return float(self._redis.get(key))

    def set_volatile_float(self, key='key-name', value=1.0):
        self._redis.set(key, value)
