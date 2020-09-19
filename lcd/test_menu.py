import time
import menu

class LCD:
    cursor_pos = (0, 0)
    columns = 16
    cursor_mode = 'hide'
    def clear(self):
        pass
    def write_string(self, message='hi'):
        pass
        
class WiFi:
    def get_ip(self):
        return '10.0.0.58'
    def scan(self):
        return []
    def decode_name(self, name):
        return name
    def add(self, ssid, password):
        pass
    def known(self):
        return []
    def remove(self, ssid):
        pass
    
class Buttons:
    def __init__(self):
        self._tic = time.time()
    def await_unclick(self):
        while self.yes or self.no or self.up or self.down:
            time.sleep(0.001)
    @property
    def a(self):
        return False
    @property
    def b(self):
        return False
    @property
    def up(self):
        return False
    @property
    def down(self):
        return False
    @property
    def left(self):
        return False
    @property
    def right(self):
        return False
    @property
    def yes(self):
        return self.right or self.a
    @property
    def no(self):
        return self.left or self.b
    @property
    def any(self):
        return self.up or self.down or self.left or self.right or self.a or self.b
    
class Update:
    def get_current_release(self):
        return ''
    def get_releases(self):
        return []
    def install(self, release='v1.0.0', update_callback=lambda text: ()):
        pass    
    
def test_startup():
    fn, _ = menu.startup({'lcd': LCD(), 'update': Update()})
    assert fn == menu.home
    
def test_home():
    class B(Buttons):
        @property
        def a(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2
        
    fn, _ = menu.home({'lcd': LCD(), 'buttons': B(), 'wifi': WiFi()})
    assert fn == menu.menu
    
def test_menu():
    class B1(Buttons):
        @property
        def a(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2
        
    fn, _ = menu.menu({'lcd': LCD(), 'buttons': B1()})
    assert fn == menu.rec
    
    class B2(Buttons):
        @property
        def down(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2
        
        @property
        def a(self):
            return self._tic + 0.5 < time.time() < self._tic + 0.6
        
    fn, _ = menu.menu({'lcd': LCD(), 'buttons': B2()})
    assert fn == menu.wifi
    
    class B3(Buttons):
        @property
        def left(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2
        
    fn, _ = menu.menu({'lcd': LCD(), 'buttons': B3()})
    assert fn == menu.home
    
def test_rec():
    class B1(Buttons):
        @property
        def right(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2
        
    fn, _ = menu.rec({'lcd': LCD(), 'buttons': B1()})
    assert fn == menu.home
    
    class B2(Buttons):
        @property
        def b(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2
        
    fn, _ = menu.rec({'lcd': LCD(), 'buttons': B2()})
    assert fn == menu.menu
    
def test_wifi():
    class B1(Buttons):
        @property
        def right(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2
        
    fn, _ = menu.wifi({'lcd': LCD(), 'buttons': B1()})
    assert fn == menu.wifi_add
    
    class B2(Buttons):
        @property
        def down(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2
        @property
        def right(self):
            return self._tic + 0.3 < time.time() < self._tic + 0.4
        
    fn, _ = menu.wifi({'lcd': LCD(), 'buttons': B2()})
    assert fn == menu.wifi_delete
    
    class B3(Buttons):
        @property
        def b(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2
        
    fn, _ = menu.wifi({'lcd': LCD(), 'buttons': B3()})
    assert fn == menu.menu
    
def test_wifi_add():
    class B1(Buttons):
        @property
        def right(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2
        
    fn, _ = menu.wifi_add({'lcd': LCD(), 'buttons': B1(), 'wifi': WiFi()})
    assert fn == menu.wifi
    
    class W1(WiFi):
        def scan(self):
            return ['ssid1', 'ssid2']
    
    class B2(Buttons):
        @property
        def down(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2
        @property
        def right(self):
            return self._tic + 0.3 < time.time() < self._tic + 0.4
        
    fn, params_out = menu.wifi_add({'lcd': LCD(), 'buttons': B2(), 'wifi': W1()})
    assert fn == menu.wifi_password
    assert params_out['ssid'] == 'ssid2'
    
    class B3(Buttons):
        @property
        def left(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2
        
    fn, _ = menu.wifi_add({'lcd': LCD(), 'buttons': B3(), 'wifi': W1()})
    assert fn == menu.wifi
    
def test_wifi_password():
    class B1(Buttons):
        @property
        def a(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2
        
    fn, _ = menu.wifi_password({'lcd': LCD(), 'buttons': B1(), 'wifi': WiFi(), 'ssid': 'ssid1'})
    assert fn == menu.home
    
    class W1(WiFi):
        def add(self, ssid, password):
            self.ssid = ssid
            self.password = password
            
    class B2(Buttons):
        @property
        def down(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2
        
        @property
        def a(self):
            return self._tic + 0.3 < time.time() < self._tic + 0.4
        
    fn, params_out = menu.wifi_password({'lcd': LCD(), 'buttons': B2(), 'wifi': W1(), 'ssid': 'ssid1'})
    assert fn == menu.home
    assert params_out['wifi'].password == '9'
    
def test_wifi_delete():
    class W1(WiFi):
        def remove(self, ssid):
            self.ssid = ssid
            
        def known(self):
            return ['ssid1', 'ssid2']
            
    class B1(Buttons):
        @property
        def down(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2
        
        @property
        def a(self):
            return self._tic + 0.3 < time.time() < self._tic + 0.4
        
    fn, params_out = menu.wifi_delete({'lcd': LCD(), 'buttons': B1(), 'wifi': W1()})
    assert fn == menu.home
    assert params_out['wifi'].ssid == 'ssid2'
    
    class B2(Buttons):
        @property
        def b(self):
            return self._tic + 0.3 < time.time() < self._tic + 0.4
        
    fn, _ = menu.wifi_delete({'lcd': LCD(), 'buttons': B2(), 'wifi': W1()})
    assert fn == menu.wifi

def test_update():
    fn, _ = menu.update({'lcd': LCD(), 'buttons': Buttons(), 'update': Update()})
    assert fn == menu.menu
    
    class U1(Update):
        def get_releases(self):
            return ['v1.0.0', 'v1.0.1']
        
    class B1(Buttons):
        @property
        def b(self):
            return self._tic + 2.3 < time.time() < self._tic + 2.4

    fn, _ = menu.update({'lcd': LCD(), 'buttons': B1(), 'update': U1()})
    assert fn == menu.menu
    
    class B2(Buttons):
        @property
        def a(self):
            return self._tic + 2.3 < time.time() < self._tic + 2.4

    fn, _ = menu.update({'lcd': LCD(), 'buttons': B2(), 'update': U1()})
    assert fn == menu.home