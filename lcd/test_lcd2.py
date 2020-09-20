import lcd2 as lcd
  
def test_cursor_pos():
    l = lcd.LCD()
    l.cursor_pos = (0, 0)
    
def test_columns():
    l = lcd.LCD()
    assert l.columns == 16
    
def test_cursor_mode():
    l = lcd.LCD()
    assert l._cursor_mode == 'hide'
    l.cursor_mode = 'hide'
    
def test_clear():
    l = lcd.LCD()
    l.clear()
    
def test_write_string():
    l = lcd.LCD()
    l.write_string('HALLO WELT')
    
if __name__ == '__main__':
    print('test_cursor_pos()')
    test_cursor_pos()    
    print('test_columns()')
    test_columns()    
    print('test_cursor_mode()')
    test_cursor_mode()    
    print('test_clear()')
    test_clear()    
    print('test_write_string()')
    test_write_string()