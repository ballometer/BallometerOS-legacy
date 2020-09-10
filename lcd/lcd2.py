import time
import menu

class LCD:
    cursor_pos = (0, 0)
    columns = 16
    cursor_mode = 'hide'
    
    def clear(self):
        pass
    
    def write_string(self, message='hi'):
        print(message)
        
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
        pass
        #while self.a or self.b or self.left or self.right or self.up or self.down:
        #    time.sleep(0.05)
        
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
    
if __name__ == '__main__':
    class B(Buttons):
        def __init__(self):
            self._tic = time.time()
            
        @property 
        def a(self):
            if time.time() - self._tic > 1.0:
                return True
            else:
                return False
        
    #fn, params = menu.startup({'lcd': LCD(), 'buttons': B(), 'wifi': WiFi()})
    
    class B2(Buttons):
        def __init__(self):
            self._tic = time.time()
            
        @property 
        def a(self):
            if time.time() - self._tic > 1.0:
                return True
            else:
                return False
            
        @property 
        def down(self):
            if (0.25 < time.time() - self._tic < 0.3) or (0.5 < time.time() - self._tic < 0.6):
                return True
            else:
                return False
            
    #menu.choose(lcd=LCD(), buttons=B2(), items=['hallo', 'welt', 'ala'])
    
    class B3(Buttons):
        def __init__(self):
            self._tic = time.time()
            
        @property 
        def a(self):
            if time.time() - self._tic > 0.4:
                return True
            else:
                return False
            
        @property 
        def down(self):
            if (0.25 < time.time() - self._tic < 0.3) or (0.5 < time.time() - self._tic < 0.6):
                return True
            else:
                return False
            
    #menu.menu({'lcd': LCD(), 'buttons': B3(), 'wifi': WiFi()})
    
    
    class B4(Buttons):
        @property 
        def a(self):
            return time.time() - self._tic > 0.7 
        @property 
        def down(self):
            return (0.25 < time.time() - self._tic < 0.3) or (0.5 < time.time() - self._tic < 0.6)
            
    #menu.rec({'lcd': LCD(), 'buttons': B4()})