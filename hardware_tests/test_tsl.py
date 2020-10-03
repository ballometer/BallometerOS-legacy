import tsl

def test_visible():
    t = tsl.TSL()
    assert 0.0 <= t.visible
    
def test_infrared():
    t = tsl.TSL()
    assert 0.0 <= t.infrared
    

if __name__ == '__main__':
    test_visible()
    test_infrared()
    