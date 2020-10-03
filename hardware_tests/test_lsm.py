import ballometer


def test_accel_x():
    lsm = ballometer.LSM()
    assert -20.0 < lsm.accel_x < 20.0


def test_accel_y():
    lsm = ballometer.LSM()
    assert -20.0 < lsm.accel_y < 20.0


def test_accel_z():
    lsm = ballometer.LSM()
    assert -20.0 < lsm.accel_z < 20.0


def test_mag_x():
    lsm = ballometer.LSM()
    assert -1e-3 < lsm.mag_x < 1e-3


def test_mag_y():
    lsm = ballometer.LSM()
    assert -1e-3 < lsm.mag_y < 1e-3


def test_mag_z():
    lsm = ballometer.LSM()
    assert -1e-3 < lsm.mag_z < 1e-3
