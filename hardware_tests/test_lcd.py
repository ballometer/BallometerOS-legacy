import ballometer


def test_cursor_pos():
    lcd = ballometer.LCD()
    lcd.cursor_pos = (0, 0)


def test_columns():
    lcd = ballometer.LCD()
    assert lcd.columns == 16


def test_cursor_mode():
    lcd = ballometer.LCD()
    assert lcd.cursor_mode == 'hide'
    lcd.cursor_mode = 'hide'


def test_clear():
    lcd = ballometer.LCD()
    lcd.clear()


def test_write_string():
    lcd = ballometer.LCD()
    lcd.write_string('HALLO WELT')
