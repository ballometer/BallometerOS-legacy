import lsm

def test_accel_x():
    l = lsm.LSM()
    assert -20.0 < l.accel_x < 20.0
    
def test_accel_y():
    l = lsm.LSM()
    assert -20.0 < l.accel_y < 20.0
    
def test_accel_z():
    l = lsm.LSM()
    assert -20.0 < l.accel_z < 20.0
    
def test_mag_x():
    l = lsm.LSM()
    assert -1e-3 < l.mag_x < 1e-3
    
def test_mag_y():
    l = lsm.LSM()
    assert -1e-3 < l.mag_y < 1e-3
    
def test_mag_z():
    l = lsm.LSM()
    assert -1e-3 < l.mag_z < 1e-3
    
if __name__ == '__main__':
    test_accel_x()
    test_accel_y()
    test_accel_z()
    test_mag_x()
    test_mag_y()
    test_mag_z()