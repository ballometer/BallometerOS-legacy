import time

def _choose(lcd, buttons, items=['item1', 'item2']):
    i = 0
    while True:
        lcd.cursor_pos = (1, 0)
        text = '>' + items[i]
        text += ' ' * (lcd.columns - len(text))
        lcd.write_string(text)
    
        buttons.await_unclick()
        
        while True:
                
            if (i > 0) and buttons.up:
                i -= 1
                break
            
            if (i < len(items) - 1) and buttons.down:
                i += 1
                break
            
            if buttons.yes or buttons.no:
                return i
            
def startup(params):
    lcd = params['lcd']
    
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string('HELLO FROM\r\nBALLOMETER')    
    time.sleep(1.0) 
    
    return home, params
    
def home(params):
    lcd = params['lcd']
    w = params['wifi']
    buttons = params['buttons']   
    
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    
    last_ip = w.get_ip()
    
    lcd.write_string(last_ip + '\r\n>MENU')

    check_ip_interval = 10 # s
    last_ip_check = time.time()
    
    buttons.await_unclick()
    
    while not buttons.yes:
        if last_ip_check + check_ip_interval < time.time():
            ip = w.get_ip()
            
            if ip != last_ip:
                last_ip = ip
                lcd.cursor_pos = (0, 0)
                text = ip
                text += ' ' * (lcd.columns - len(text))
                lcd.write_string(text)
                
            last_ip_check = time.time()
    
    return menu, params
            
def menu(params):
    lcd = params['lcd']
    buttons = params['buttons']
    
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string('MENU')
    
    items = ['REC', 'WIFI']
    
    buttons.await_unclick()
    
    item = items[_((lcd=lcd, buttons=buttons, items=items)]
    
    if buttons.no:
        return home, params
    
    if item == 'REC':
        return rec, params
    elif item == 'WIFI':
        return wifi, params
    else:
        # raise error
        pass
    
def rec(params):
    lcd = params['lcd']
    buttons = params['buttons']
    
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string('REC')
    
    items = ['START', 'CONTINUE', 'STOP']
    
    buttons.await_unclick()
    
    item = items[_((lcd=lcd, buttons=buttons, items=items)]
    
    if buttons.no:
        return menu, params
    
    if item == 'START':
        # start recording
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('START REC...')
    elif item == 'CONTINUE':
        # continue recording
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('CONNTINUE\r\nREC...')
    elif item == 'STOP':
        # stop recording
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('STOP REC...')
    
    return home, params
    
def wifi(params):
    lcd = params['lcd']
    buttons = params['buttons']
    
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string('WIFI')
    
    items = ['ADD', 'DELETE']
    
    buttons.await_unclick()
    
    item = items[_((lcd=lcd, buttons=buttons, items=items)]
    
    if buttons.no:
        return menu, params
    
    if item == 'ADD':
        return wifi_add, params
    elif item == 'DELETE':
        return wifi_delete, params
    
def wifi_add(params):
    lcd = params['lcd']
    buttons = params['buttons']
    w = params['wifi']
    
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string('SCANNING...')
    
    ssids = w.scan()
    
    if len(ssids) == 0:
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        text = 'NO WIFI\r\nFOUND...'
        lcd.write_string(text)
        time.sleep(2)
        return wifi, params
    
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    text = 'CHOOSE WIFI:'
    lcd.write_string(text)
    
    ssids_decoded = [w.decode_name(name) for name in ssids]
    
    i = _choose(lcd=lcd, buttons=buttons, items=ssids_decoded)
    
    if buttons.no:
        return wifi, params
    
    params['ssid'] = ssids[i]
    return wifi_password, params

def wifi_password(params):
    lcd = params['lcd']
    buttons = params['buttons']
    w = params['wifi']
    ssid = params['ssid']
    
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    text = 'PASSWORD:'
    lcd.write_string(text)
    
    password_max_length = 64
    password_codes = [0 for _ in range(password_max_length)]
    
    cursor = 0
    shift = 0
    
    lcd.cursor_mode = 'line'
    lcd.cursor_pos = (1, cursor)
    buttons.await_unclick()
    
    letters = [
        ' ',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 
        'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 
        'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 
        'W', 'X', 'Y', 'Z', '.', ',', 
        '?', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', '-', '/', ':', ';', 
        '<', '=', '>', '@', '[', ']', '^', '_', '`', '{', '|', '}',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    ]
    
    while True:
        while True:
            begin_press = True
            while buttons.up:
                password_codes[cursor + shift] = password_codes[cursor + shift] + 1
                password_codes[cursor + shift] %= len(letters)
                lcd.write_string(letters[password_codes[cursor + shift]])
                lcd.cursor_pos = (1, cursor)
                
                if begin_press:
                    time.sleep(0.2)
                    begin_press = False
                else:
                    time.sleep(0.05)
                
                
            while buttons.down:
                password_codes[cursor + shift] = password_codes[cursor + shift] - 1
                password_codes[cursor + shift] %= len(letters)
                lcd.write_string(letters[password_codes[cursor + shift]])
                lcd.cursor_pos = (1, cursor)
                
                if begin_press:
                    time.sleep(0.2)
                    begin_press = False
                else:
                    time.sleep(0.05)
                    
            if buttons.left:
                if cursor > 0:
                    cursor -= 1
                    lcd.cursor_pos = (1, cursor)
                    time.sleep(0.3)
                    break
                elif cursor + shift > 0:
                    shift -= 1
                    lcd.cursor_pos = (1, 0)
                    text = ''.join([letters[code] for code in password_codes[shift:(shift + lcd.columns)]])
                    lcd.write_string(text)
                    lcd.cursor_pos = (1, cursor)
                    time.sleep(0.3)
                    break        
            
            if buttons.right:
                if cursor < lcd.columns - 1:
                    cursor += 1
                    lcd.cursor_pos = (1, cursor)
                    time.sleep(0.3)
                    break
                elif cursor + shift < password_max_length - 1:
                    shift += 1
                    lcd.cursor_pos = (1, 0)
                    text = ''.join([letters[code] for code in password_codes[shift:(shift + lcd.columns)]])
                    lcd.write_string(text)
                    lcd.cursor_pos = (1, cursor)
                    time.sleep(0.3)
                    break              
            
            if buttons.a or buttons.b:
                break
        
        if buttons.a or buttons.b:
            break
             
    lcd.cursor_mode = 'hide'
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    
    if buttons.a:
        lcd.write_string('CONNECTING...')
        time.sleep(0.75)
        password = ''.join([letters[code] for code in password_codes]).strip()
        w.add(ssid, password)
    else:
        lcd.write_string('CANCEL...')
        time.sleep(1)
    
    return home, params
    

def wifi_delete(params):
    lcd = params['lcd']
    w = params['wifi']
    buttons = params['buttons']
    
    wifis = w.known()
        
    if len(wifis) == 0:
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        text = 'NO WIFI\r\nSTORED...'
        lcd.write_string(text)
        time.sleep(2)
        return wifi, params
        
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    text = 'DELETE WIFI:'
    lcd.write_string(text)
        
    i = _choose((lcd=lcd, buttons=buttons, items=wifis)
        
    if buttons.no:
        return wifi, params
        
    w.remove(wifis[i])
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    text = 'DELETED:\r\n' + wifis[i]
    lcd.write_string(text)
    time.sleep(2)
    
    return home, params