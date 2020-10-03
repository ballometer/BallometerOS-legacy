import ballometer

lcd = ballometer.LCD()
buttons = ballometer.Buttons()

fn, params = ballometer.menu.startup({
    'lcd': lcd,
    'buttons': buttons,
})

while True:
    fn, params = fn(params)
