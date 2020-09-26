import bmp

def test_temperature():
    b = bmp.BMP()
    assert 250.0 < b.temperature < 350.0
    
def test_pressure():
    b = bmp.BMP()
    assert 300.0 * 1e2 < b.pressure < 1100.0 * 1e2
    
if __name__ == '__main__':
    test_temperature()
    test_pressure()