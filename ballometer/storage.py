import influxdb
import time


class Store:
    def __init__(self):
        self._db_name = 'ballometer'
        self._client = influxdb.InfluxDBClient()
        if self._client.switch_database(self._db_name) is None:
            self._client.create_database(self._db_name)

    def save(self, key='key-name', value=1.0, unixtime=None):
        if unixtime is None:
            unixtime = time.time()

        if unixtime < 1601116701:
            # The system time is not synchronized yet
            # and is probably still at the default value
            # in year 1970. Skip writing to influxdb.
            return

        self._client.write_points([
            {
                'measurement': key,
                'fields': {
                    'value': float(value)
                },
                'time': unixtime
            }
        ])
