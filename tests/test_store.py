import ballometer


def test_constructor(mocker):
    mocker.patch('redis.Redis.ping')
    mocker.patch('influxdb.InfluxDBClient.ping')
    mocker.patch('redis.Redis.get')
    mocker.patch('redis.Redis.set')
    mocker.patch('influxdb.InfluxDBClient.query')
    ballometer.Store()


def test_clock_was_synchronized(mocker):
    mocker.patch('redis.Redis.ping')
    mocker.patch('influxdb.InfluxDBClient.ping')
    mocker.patch('redis.Redis.get')
    mocker.patch('redis.Redis.set')
    mocker.patch('influxdb.InfluxDBClient.query')
    store = ballometer.Store()

    assert store.clock_was_synchronized() is True

    mocker.patch('time.time', return_value=0.0)
    assert store.clock_was_synchronized() is False


def test_save(mocker):
    mocker.patch('redis.Redis.ping')
    mocker.patch('influxdb.InfluxDBClient.ping')
    mocker.patch('redis.Redis.get')
    mocker.patch('redis.Redis.set')
    mocker.patch('influxdb.InfluxDBClient.query')
    store = ballometer.Store()

    mocker.patch('redis.Redis.publish')
    mocker.patch('influxdb.InfluxDBClient.write_points')

    store.save(key='bmp_pressure', value=94034.0)
