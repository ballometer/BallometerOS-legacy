import wifi

def test_decode_name():
    w = wifi.WiFi()
    assert w.decode_name('t\\xC3\\xA9st') == 'tést'
    
def test_get_ip():
    w = wifi.WiFi()
    assert isinstance(w.get_ip(), str)
    
def test_scan():
    '''
    This test assumes that there is an access point with the ssid set to "android-ballometer".
    '''
    w = wifi.WiFi()
    assert 'android-ballometer' in w.scan()
    
def test_add():
    '''
    This test assumes that there is an access point with the ssid set to "android-ballometer"
    and the password is "abba9889".
    '''
    w = wifi.WiFi()
    w.add(ssid='android-ballometer', password='abba9889')
    
def test_known():
    '''
    This test assumes that you have previously added a network with ssid "android-ballometer".
    '''
    w = wifi.WiFi()
    assert 'android-ballometer' in w.known()
    
def test_remove():
    w = wifi.WiFi()
    w.remove('android-ballometer')
    
def test_reset():
    w = wifi.WiFi()
    w.reset()
    
if __name__ == '__main__':
    print('test_decode_name')
    test_decode_name()
    print('test_get_ip')
    test_get_ip()
    print('test_scan')
    test_scan()
    print('test_add')
    test_add()
    print('test_known')
    test_known()
    print('test_remove')
    test_remove()
    print('test_reset')
    test_reset()
    
