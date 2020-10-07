import influxdb
import redis
import time
import requests
import json


class Store:
    def __init__(self):
        '''
        This constructor is blocking until both influxdb
        and redis respond to ping. This is useful during system
        startup. When the constructor returns, the storage system
        is ready to use.
        '''

        self._db_name = 'ballometer'
        self._influx = influxdb.InfluxDBClient()
        if self._influx.switch_database(self._db_name) is None:
            self._influx.create_database(self._db_name)

        self._redis = redis.Redis()

        while True:
            try:
                self._influx.ping()
                self._redis.ping()
                break
            except requests.exceptions.ConnectionError:
                print('InfluxDB is not ready')
                time.sleep(5)
            except redis.exceptions.ConnectionError:
                print('Redis is not ready')
                time.sleep(5)

        if self._redis.get('flight_id') is None:
            # Volatile redis key has not been set yet.
            # Get it from influxdb.
            flight_id = self._get_max_flight_id()
            self._set_volatile_float('flight_id', float(flight_id))

        if self._redis.get('qnh') is None:
            # Volatile redis key has not been set yet.
            # Get it from influxdb.
            qnh = self._get_last_qnh()
            self._set_volatile_float('qnh', float(qnh))

    def clock_was_synchronized(self):
        return time.time() > 1601116701.0

    def save(self, key='key-name', value=1.0, unixtime=None):
        '''
        Stores data permanently in influxdb if the system clock has been
        synchronized (and is not at 1970 any more) and recording has
        been turned on.
        '''
        if unixtime is None:
            unixtime = time.time()

        serialized = json.dumps({'value': value, 'unixtime': unixtime})
        redis_key = f'save:{key}'
        self._redis.publish(redis_key, serialized)
        self._redis.set(redis_key, serialized)
        self._redis.sadd('save', key)

        if not self.clock_was_synchronized():
            # The system time is not synchronized yet
            # and is probably still at the default value
            # in year 1970. Skip writing to influxdb.
            return

        if not self.recording:
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
                    'flight_id': str(self.flight_id)
                }
            }
        ])

    def get_saved(self):
        '''
        Returns for all the keys the last value that was
        saved in the format
        {
            'bmp_pressure': {
                'value': 98443.0,
                'unixtime': 123456.0
            },
            'sht_temperature': {
                'value': 302.1,
                'unixtime': 123456.0
            },
            ...
        }
        '''
        return {
            key.decode(): json.loads(self._redis.get(f'save:{key}'))
            for key in self._redis.smembers('save')
        }

    def _get_volatile_float(self, key='key-name'):
        value = self._redis.get(key)
        if value is None:
            return 0.0
        return float(value)

    def _set_volatile_float(self, key='key-name', value=1.0):
        self._redis.set(key, str(float(value)))

    def _get_max_flight_id(self) -> int:
        q = self._influx.query('SHOW TAG VALUES WITH KEY = "flight_id"')
        # list(q.get_points()) is [{'key': 'flight_id', 'value': '1'}, ...]
        values = [int(point['value']) for point in q.get_points()]
        if len(values) == 0:
            return 0
        return max(values)

    def _get_last_qnh(self) -> int:
        q = self._influx.query(
            'SELECT "value" FROM "qnh" ORDER BY DESC LIMIT 1')
        # list(q.get_points()) is
        # [{'time': '2020-10-03T18:10:00Z', 'value': 1018.0}]
        values = [int(point['value']) for point in q.get_points()]
        if len(values) == 0:
            return 1013
        return values[0]

    @property
    def recording(self) -> bool:
        return bool(self._get_volatile_float('recording'))

    @recording.setter
    def recording(self, value: bool):
        self._set_volatile_float('recording', float(value))

    @property
    def flight_id(self) -> int:
        return int(self._get_volatile_float('flight_id'))

    @flight_id.setter
    def flight_id(self, value: int):
        self._set_volatile_float('flight_id', float(value))

    @property
    def qnh(self) -> int:
        return int(self._get_volatile_float('qnh'))

    @qnh.setter
    def qnh(self, value: int):
        self.save('qnh', float(value))
        self._set_volatile_float('qnh', float(value))
