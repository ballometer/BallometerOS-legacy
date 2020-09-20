import menu
import lcd
import buttons
import wifi
import update

fn, params = menu.startup({
    'lcd': lcd.LCD(),
    'buttons': buttons.Buttons(),
    'wifi': wifi.WiFi(),
    'update': update.Update()
})

while True:
    fn, params = fn(params)
    