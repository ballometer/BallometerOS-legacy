from . import test_bmp
from . import test_lcd
from . import test_lsm
from . import test_sht
from . import test_tsl
from . import test_update
from . import test_wifi


print('###### test_bmp')
test_bmp.test_all()

print('###### test_lcd')
test_lcd.test_all()

print('###### test_lsm')
test_lsm.test_all()

print('###### test_sht')
test_sht.test_all()

print('###### test_tsl')
test_tsl.test_all()

print('###### test_update')
test_update.test_all()

print('###### test_wifi')
test_wifi.test_all()
