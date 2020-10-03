import ballometer


def test_visible():
    tsl = ballometer.TSL()
    assert 0.0 <= tsl.visible


def test_infrared():
    tsl = ballometer.TSL()
    assert 0.0 <= tsl.infrared
