import time
from RPLCD.i2c import CharLCD
import os
import json
from statemachine import StateMachine, State

import wifi
import buttons

lcd_columns = 16
lcd_rows = 2

lcd = CharLCD('PCF8574', 0x27)
buttons = buttons.Buttons()

flight_id_path = os.path.dirname(os.path.realpath(__file__)) + '/flight_id.json'

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

def await_unclick(buttons):
    while buttons.any:
        time.sleep(0.01)

class BallometerLCD(StateMachine):
    
    ssid = ''
    password = ''
    
    # states
    
    greeting = State('greeting', initial=True)
    
    home = State('home')
    
    menu_rec = State('menu_rec')
    menu_wifi = State('menu_wifi')

    rec_start = State('rec_start')
    rec_stop = State('rec_stop')
    rec_continue = State('rec_continue')
    
    wifi_add = State('wifi_add')
    wifi_delete = State('wifi_delete')
    
    choose_wifi = State('choose_wifi')
    password_wifi = State('password_wifi')
    delete_wifi = State('delete_wifi')
    
    # transitions
    
    greeting_to_home = greeting.to(home)
        
    home_to_menu_rec = home.to(menu_rec)
    
    menu_rec_to_wifi = menu_rec.to(menu_wifi)
    menu_rec_to_home = menu_rec.to(home)
    menu_rec_to_rec_start = menu_rec.to(rec_start)
    
    menu_wifi_to_rec = menu_wifi.to(menu_rec)
    menu_wifi_to_home = menu_wifi.to(home)
    menu_wifi_to_wifi_add = menu_wifi.to(wifi_add)
    
    rec_start_to_stop = rec_start.to(rec_stop)
    rec_start_to_home = rec_start.to(home)
    rec_start_to_menu_rec = rec_start.to(menu_rec)
    
    rec_stop_to_start = rec_stop.to(rec_start)
    rec_stop_to_continue = rec_stop.to(rec_continue)
    rec_stop_to_home = rec_stop.to(home)
    rec_stop_to_menu_rec = rec_stop.to(menu_rec)
    
    rec_continue_to_stop = rec_continue.to(rec_stop)
    rec_continue_to_home = rec_continue.to(home)
    rec_continue_to_menu_rec = rec_continue.to(menu_rec)
    
    wifi_add_to_delete = wifi_add.to(wifi_delete)
    wifi_add_to_menu_wifi = wifi_add.to(menu_wifi)
    wifi_add_to_choose_wifi = wifi_add.to(choose_wifi)
    
    wifi_delete_to_add = wifi_delete.to(wifi_add)
    wifi_delete_to_menu_wifi = wifi_delete.to(menu_wifi)
    wifi_delete_to_delete_wifi = wifi_delete.to(delete_wifi)
    
    choose_wifi_to_password_wifi = choose_wifi.to(password_wifi)
    choose_wifi_to_wifi_add = choose_wifi.to(wifi_add)
    
    password_wifi_to_home = password_wifi.to(home)
    
    delete_wifi_to_wifi_delete = delete_wifi.to(wifi_delete)
    delete_wifi_to_home = delete_wifi.to(home)
    
    
    
    #
    # on transitions
    # 
    
    def on_greeting_to_home(self):
        nickname = ''
        nickname_path = os.path.dirname(os.path.realpath(__file__)) + '/nickname.json'
        
        with open(nickname_path) as f:
            nickname = json.load(f)['nickname'].strip().upper()
        
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('BALLOMETER:\r\nHI ' + nickname)
        
        time.sleep(1.0)
        
    def on_home_to_menu_rec(self):
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('MENU:')          
        
    def on_rec_start_to_menu_rec(self):
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('MENU:')
        
    def on_rec_stop_to_menu_rec(self):
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('MENU:')
        
    def on_rec_continue_to_menu_rec(self):
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('MENU:')
        
    def on_wifi_add_to_menu_wifi(self):
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('MENU:')
        
    def on_wifi_delete_to_menu_wifi(self):
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('MENU:')
        
    def on_menu_rec_to_rec_start(self):
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('REC:')
        
    def on_menu_wifi_to_wifi_add(self):
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('WIFI:')
        
    def on_choose_wifi_to_wifi_add(self):
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('WIFI:')
        
    def on_delete_wifi_to_wifi_delete(self):
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('WIFI:')
        
    def on_rec_start_to_home(self):
        data = {}
        
        with open(flight_id_path) as f:
            data = json.load(f)
            
        data['flight_id'] = int(data['flight_id']) + 1
        data['recording'] = True
        
        with open(flight_id_path, 'w') as f:
            json.dump(data, f)
        
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('START\r\nRECORDING...')
        time.sleep(0.75)
        
    def on_rec_stop_to_home(self):
        data = {}
        
        with open(flight_id_path) as f:
            data = json.load(f)
            
        data['recording'] = False
        
        with open(flight_id_path, 'w') as f:
            json.dump(data, f)
        
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('STOP\r\nRECORDING...')
        time.sleep(0.75)
        
    def on_rec_continue_to_home(self):
        data = {}
        
        with open(flight_id_path) as f:
            data = json.load(f)
            
        data['recording'] = True
        
        with open(flight_id_path, 'w') as f:
            json.dump(data, f)
        
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('CONTINUE\r\nRECORDING...')
        time.sleep(0.75)
        
    # 
    # on enter states 
    #
    
    def on_enter_home(self):
        
        recording = False
        
        with open(flight_id_path) as f:
            data = json.load(f)
            recording = data['recording']
                    
        
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        
        last_ip = wifi.get_ip()
        
        if recording:
            lcd.write_string(last_ip + '\r\n>MENU        REC')
        else:
            lcd.write_string(last_ip + '\r\n>MENU')

        check_ip_interval = 10 # s
        last_ip_check = time.time()
        
        rec_blink_off_interval = 0.25
        rec_blink_on_interval = 1
        rec_blink = False
        rec_blink_last = time.time()
        
        await_unclick(buttons)
        
        while not buttons.yes:
            if last_ip_check + check_ip_interval < time.time():
                ip = wifi.get_ip()
                
                if ip != last_ip:
                    last_ip = ip
                    lcd.cursor_pos = (0, 0)
                    text = ip
                    text += ' ' * (lcd_columns - len(text))
                    lcd.write_string(text)
                    
                last_ip_check = time.time()
                
            if recording:
                if rec_blink and (rec_blink_last + rec_blink_on_interval < time.time()):
                    rec_blink = False
                    rec_blink_last = time.time()
                    lcd.cursor_pos = (1, 12)
                    lcd.write_string(' ')
                if not rec_blink and (rec_blink_last + rec_blink_off_interval < time.time()):
                    rec_blink = True
                    rec_blink_last = time.time()
                    lcd.cursor_pos = (1, 12)
                    lcd.write_string('*')
        
        if buttons.yes:
            self.home_to_menu_rec()
            
    def on_enter_menu_rec(self):
        time.sleep(0.1)
        lcd.cursor_pos = (1, 0)
        text = '>REC'
        text += ' ' * (lcd_columns - len(text))
        lcd.write_string(text)
        
        await_unclick(buttons)
        
        while not (buttons.down or buttons.yes or buttons.no):
            pass
        
        if buttons.down:
            self.menu_rec_to_wifi()
        
        if buttons.yes:
            self.menu_rec_to_rec_start()
            
        if buttons.no:
            self.menu_rec_to_home()
            
    def on_enter_menu_wifi(self):
        lcd.cursor_pos = (1, 0)
        text = '>WIFI'
        text += ' ' * (lcd_columns - len(text))
        lcd.write_string(text)
        
        await_unclick(buttons)
        
        while not (buttons.up or buttons.yes or buttons.no):
            pass
        
        if buttons.up:
            self.menu_wifi_to_rec()
             
        if buttons.no:
            self.menu_wifi_to_home()
            
        if buttons.yes:
            self.menu_wifi_to_wifi_add()
    
    def on_enter_rec_start(self):
        lcd.cursor_pos = (1, 0)
        text = '>START'
        text += ' ' * (lcd_columns - len(text))
        lcd.write_string(text)
        
        await_unclick(buttons)
        
        while not (buttons.down or buttons.yes or buttons.no):
            pass
        
        if buttons.down:
            self.rec_start_to_stop()
            
        if buttons.yes:
            self.rec_start_to_home()
            
        if buttons.no:
            self.rec_start_to_menu_rec()
            
    def on_enter_rec_stop(self):
        lcd.cursor_pos = (1, 0)
        text = '>STOP'
        text += ' ' * (lcd_columns - len(text))
        lcd.write_string(text)
        
        await_unclick(buttons)
        
        while not buttons.any:
            pass
        
        if buttons.down:
            self.rec_stop_to_continue()
            
        if buttons.up:
            self.rec_stop_to_start()
            
        if buttons.yes:
            self.rec_stop_to_home()
            
        if buttons.no:
            self.rec_stop_to_menu_rec()
        
    def on_enter_rec_continue(self):
        lcd.cursor_pos = (1, 0)
        text = '>CONTINUE'
        text += ' ' * (lcd_columns - len(text))
        lcd.write_string(text)
        
        await_unclick(buttons)
        
        while not (buttons.up or buttons.yes or buttons.no):
            pass
        
        if buttons.up:
            self.rec_continue_to_stop()
            
        if buttons.yes:
            self.rec_continue_to_home()
        
        if buttons.no:
            self.rec_continue_to_menu_rec()
            
    def on_enter_wifi_add(self):
        lcd.cursor_pos = (1, 0)
        text = '>ADD'
        text += ' ' * (lcd_columns - len(text))
        lcd.write_string(text)
            
        await_unclick(buttons)
        
        while not (buttons.down or buttons.yes or buttons.no):
            pass
        
        if buttons.down:
            self.wifi_add_to_delete()
            
        if buttons.yes:
            self.wifi_add_to_choose_wifi()
            
        if buttons.no:
            self.wifi_add_to_menu_wifi()
            
    def on_enter_wifi_delete(self):
        lcd.cursor_pos = (1, 0)
        text = '>DELETE'
        text += ' ' * (lcd_columns - len(text))
        lcd.write_string(text)
        
        await_unclick(buttons)
        
        while not (buttons.up or buttons.yes or buttons.no):
            pass
        
        if buttons.up:
            self.wifi_delete_to_add()
            
        if buttons.yes:
            self.wifi_delete_to_delete_wifi()
            
        if buttons.no:
            self.wifi_delete_to_menu_wifi()
            
    def on_enter_choose_wifi(self):
        
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('SCANNING...')
        
        wifis = wifi.scan()
        
        if len(wifis) == 0:
            lcd.clear()
            lcd.cursor_pos = (0, 0)
            text = 'NO WIFI\r\nFOUND...'
            lcd.write_string(text)
            time.sleep(2)
            self.choose_wifi_to_wifi_add()
            
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        text = 'CHOOSE WIFI:'
        lcd.write_string(text)
            
        i = 0
        
        await_unclick(buttons)
        while True:
            lcd.cursor_pos = (1, 0)
            text = '>' + wifi.decode_name(wifis[i])
            text += ' ' * (lcd_columns - len(text))
            lcd.write_string(text)
            
           
            await_unclick(buttons)
            while True:
                 
                if (i > 0) and buttons.up:
                    i -= 1
                    break
                
                if (i < len(wifis) - 1) and buttons.down:
                    i += 1
                    break
                
                if buttons.yes or buttons.no:
                    break
                
            if buttons.yes or buttons.no:
                break
            
        if buttons.no:
            self.choose_wifi_to_wifi_add()
            
        if buttons.yes:
            self.ssid = wifis[i]
            self.choose_wifi_to_password_wifi()
                
            
            
    def on_enter_password_wifi(self):
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
        
        await_unclick(buttons)
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
                        text = ''.join([letters[code] for code in password_codes[shift:(shift + lcd_columns)]])
                        lcd.write_string(text)
                        lcd.cursor_pos = (1, cursor)
                        time.sleep(0.3)
                        break        
                
                if buttons.right:
                    if cursor < lcd_columns - 1:
                        cursor += 1
                        lcd.cursor_pos = (1, cursor)
                        time.sleep(0.3)
                        break
                    elif cursor + shift < password_max_length - 1:
                        shift += 1
                        lcd.cursor_pos = (1, 0)
                        text = ''.join([letters[code] for code in password_codes[shift:(shift + lcd_columns)]])
                        lcd.write_string(text)
                        lcd.cursor_pos = (1, cursor)
                        time.sleep(0.3)
                        break              
                
                if buttons.a or buttons.b:
                    break
                
            if buttons.a:
                self.password = ''.join([letters[code] for code in password_codes]).strip()
                break
            
            if buttons.b:
                lcd.cursor_mode = 'hide'
                lcd.clear()
                lcd.cursor_pos = (0, 0)
                lcd.write_string('CANCEL...')
                time.sleep(1)
                self.password_wifi_to_home()
                
        lcd.cursor_mode = 'hide'
        
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('CONNECTING...')
        time.sleep(0.75)
        
        connected = wifi.add(self.ssid, self.password)
        
        if connected:
            lcd.clear()
            lcd.cursor_pos = (0, 0)
            lcd.write_string('PASSWORD OK')
            time.sleep(1)
            self.password_wifi_to_home()
        else:
            lcd.clear()
            lcd.cursor_pos = (0, 0)
            lcd.write_string('PASSWORD WRONG')
            time.sleep(1)
            self.password_wifi_to_home()
        
        
            
                    
                    
                        
                    
    def on_enter_delete_wifi(self):
        wifis = wifi.known()
        
        if len(wifis) == 0:
            lcd.clear()
            lcd.cursor_pos = (0, 0)
            text = 'NO WIFI\r\nSTORED...'
            lcd.write_string(text)
            time.sleep(2)
            self.delete_wifi_to_wifi_delete()
            
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        text = 'DELETE WIFI:'
        lcd.write_string(text)
            
        i = 0
        
        await_unclick(buttons)
        while True:
            lcd.cursor_pos = (1, 0)
            text = '>' + wifi.decode_name(wifis[i])
            text += ' ' * (lcd_columns - len(text))
            lcd.write_string(text)
            
            await_unclick(buttons)
            while True:
                
                if (i > 0) and buttons.up:
                    i -= 1
                    break
                
                if (i < len(wifis) - 1) and buttons.down:
                    i += 1
                    break
                
                if buttons.yes or buttons.no:
                    break
                
            if buttons.yes or buttons.no:
                break
            
        if buttons.no:
            self.delete_wifi_to_wifi_delete()
            
        if buttons.yes:
            wifi.remove(wifis[i])
            lcd.clear()
            lcd.cursor_pos = (0, 0)
            text = 'DELETED:\r\n' + wifis[i]
            lcd.write_string(text)
            time.sleep(2)
            self.delete_wifi_to_home()
            
    



def turn_off_recording():
    data = {
        'flight_id': 0,
        'recording': False
    }

    with open(flight_id_path) as f:
        data = json.load(f)
        
    data['recording'] = False
                
    with open(flight_id_path, 'w') as f:
        json.dump(data, f) 
        
        
turn_off_recording()

m = BallometerLCD()
m.greeting_to_home()
