import sht

def test_temperature():
    s = sht.SHT()
    assert 250 < s.temperature < 350
    
def test_humidity():
    s = sht.SHT()
    assert 0 <= s.humidity <= 100
    
if __name__ == '__main__':
    test_temperature()
    test_humidity()
    