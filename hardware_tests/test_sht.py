import ballometer


def test_temperature():
    sht = ballometer.SHT()
    assert 250 < sht.temperature < 350


def test_humidity():
    sht = ballometer.SHT()
    assert 0 <= sht.humidity <= 100
