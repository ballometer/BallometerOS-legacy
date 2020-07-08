import time
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import os
import json
from statemachine import StateMachine, State
from wifi import scanWifis, knownWifis, connectWifi, deleteWifi, getIP, decodeName


lcd_columns = 16
lcd_rows = 2

i2c = busio.I2C(board.SCL, board.SDA)

lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

flight_id_path = os.path.dirname(os.path.realpath(__file__)) + '/flight_id.json'

def any_button():
    return lcd.up_button or lcd.down_button or lcd.left_button or lcd.right_button or lcd.select_button

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
        lcd.cursor_position(column=0, row=0)
        lcd.message = 'BALLOMETER:\nHELLO ' + nickname
        
        time.sleep(1)
        
    def on_home_to_menu_rec(self):
        lcd.clear()
        lcd.cursor_position(column=0, row=0)
        lcd.message = 'MENU:'          
        
    def on_rec_start_to_menu_rec(self):
        lcd.clear()
        lcd.cursor_position(column=0, row=0)
        lcd.message = 'MENU:'
        
    def on_rec_stop_to_menu_rec(self):
        lcd.clear()
        lcd.cursor_position(column=0, row=0)
        lcd.message = 'MENU:'
        
    def on_rec_continue_to_menu_rec(self):
        lcd.clear()
        lcd.cursor_position(column=0, row=0)
        lcd.message = 'MENU:'
        
    def on_wifi_add_to_menu_wifi(self):
        lcd.clear()
        lcd.cursor_position(column=0, row=0)
        lcd.message = 'MENU:'
        
    def on_wifi_delete_to_menu_wifi(self):
        lcd.clear()
        lcd.cursor_position(column=0, row=0)
        lcd.message = 'MENU:'
        
    def on_menu_rec_to_rec_start(self):
        lcd.clear()
        lcd.cursor_position(column=0, row=0)
        lcd.message = 'REC:'
        
    def on_menu_wifi_to_wifi_add(self):
        lcd.clear()
        lcd.cursor_position(column=0, row=0)
        lcd.message = 'WIFI:'
        
    def on_choose_wifi_to_wifi_add(self):
        lcd.clear()
        lcd.cursor_position(column=0, row=0)
        lcd.message = 'WIFI:'
        
    def on_delete_wifi_to_wifi_delete(self):
        lcd.clear()
        lcd.cursor_position(column=0, row=0)
        lcd.message = 'WIFI:'
        
    def on_rec_start_to_home(self):
        data = {}
        
        with open(flight_id_path) as f:
            data = json.load(f)
            
        data['flight_id'] = int(data['flight_id']) + 1
        data['recording'] = True
        
        with open(flight_id_path, 'w') as f:
            json.dump(data, f)
        
        lcd.clear()
        lcd.cursor_position(column=0, row=0)
        lcd.message = 'START\nRECORDING...'
        time.sleep(0.75)
        
    def on_rec_stop_to_home(self):
        data = {}
        
        with open(flight_id_path) as f:
            data = json.load(f)
            
        data['recording'] = False
        
        with open(flight_id_path, 'w') as f:
            json.dump(data, f)
        
        lcd.clear()
        lcd.cursor_position(column=0, row=0)
        lcd.message = 'STOP\nRECORDING...'
        time.sleep(0.75)
        
    def on_rec_continue_to_home(self):
        data = {}
        
        with open(flight_id_path) as f:
            data = json.load(f)
            
        data['recording'] = True
        
        with open(flight_id_path, 'w') as f:
            json.dump(data, f)
        
        lcd.clear()
        lcd.cursor_position(column=0, row=0)
        lcd.message = 'CONTINUE\nRECORDING...'
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
        lcd.cursor_position(column=0, row=0)
        
        last_ip = getIP()
        
        if recording:
            lcd.message = last_ip + '\n>MENU        REC' 
        else:
            lcd.message = last_ip + '\n>MENU'

        check_ip_interval = 10 # s
        last_ip_check = time.time()
        
        rec_blink_off_interval = 0.25
        rec_blink_on_interval = 1
        rec_blink = False
        rec_blink_last = time.time()
        
        while not (lcd.right_button or lcd.select_button):
            if last_ip_check + check_ip_interval < time.time():
                ip = getIP()
                
                if ip != last_ip:
                    last_ip = ip
                    lcd.cursor_position(column=0, row=0)
                    text = ip
                    text += ' ' * (lcd_columns - len(text))
                    lcd.message = text
                    
                last_ip_check = time.time()
                
            if recording:
                if rec_blink and (rec_blink_last + rec_blink_on_interval < time.time()):
                    rec_blink = False
                    rec_blink_last = time.time()
                    lcd.cursor_position(column=12, row=1)
                    lcd.message = ' '
                if not rec_blink and (rec_blink_last + rec_blink_off_interval < time.time()):
                    rec_blink = True
                    rec_blink_last = time.time()
                    lcd.cursor_position(column=12, row=1)
                    lcd.message = '*'
        
        if lcd.right_button or lcd.select_button:
            self.home_to_menu_rec()
            
    def on_enter_menu_rec(self):
        lcd.cursor_position(column=0, row=1)
        text = '>REC'
        text += ' ' * (lcd_columns - len(text))
        lcd.message = text
        
        while not (lcd.select_button or lcd.right_button or lcd.down_button or lcd.left_button):
            pass
        
        if lcd.select_button or lcd.right_button:
            self.menu_rec_to_rec_start()
            
        if lcd.down_button:
            self.menu_rec_to_wifi()
            
        if lcd.left_button:
            self.menu_rec_to_home()
            
    def on_enter_menu_wifi(self):
        lcd.cursor_position(column=0, row=1)
        text = '>WIFI'
        text += ' ' * (lcd_columns - len(text))
        lcd.message = text
        
        while not (lcd.up_button or lcd.left_button or lcd.right_button or lcd.select_button):
            pass
        
        if lcd.up_button:
            self.menu_wifi_to_rec()
             
        if lcd.left_button:
            self.menu_wifi_to_home()
            
        if lcd.right_button or lcd.select_button:
            self.menu_wifi_to_wifi_add()
    
    def on_enter_rec_start(self):
        lcd.cursor_position(column=0, row=1)
        text = '>START'
        text += ' ' * (lcd_columns - len(text))
        lcd.message = text
        
        while not (lcd.down_button or lcd.select_button or lcd.right_button or lcd.left_button):
            pass
        
        if lcd.down_button:
            self.rec_start_to_stop()
            
        if lcd.select_button or lcd.right_button:
            self.rec_start_to_home()
            
        if lcd.left_button:
            self.rec_start_to_menu_rec()
            
    def on_enter_rec_stop(self):
        lcd.cursor_position(column=0, row=1)
        text = '>STOP'
        text += ' ' * (lcd_columns - len(text))
        lcd.message = text
        
        while not any_button():
            pass
        
        if lcd.down_button:
            self.rec_stop_to_continue()
            
        if lcd.up_button:
            self.rec_stop_to_start()
            
        if lcd.select_button or lcd.right_button:
            self.rec_stop_to_home()
            
        if lcd.left_button:
            self.rec_stop_to_menu_rec()
        
    def on_enter_rec_continue(self):
        lcd.cursor_position(column=0, row=1)
        text = '>CONTINUE'
        text += ' ' * (lcd_columns - len(text))
        lcd.message = text
        
        while not (lcd.up_button or lcd.right_button or lcd.select_button or lcd.left_button):
            pass
        
        if lcd.up_button:
            self.rec_continue_to_stop()
            
        if lcd.select_button or lcd.right_button:
            self.rec_continue_to_home()
        
        if lcd.left_button:
            self.rec_continue_to_menu_rec()
            
    def on_enter_wifi_add(self):
        lcd.cursor_position(column=0, row=1)
        text = '>ADD'
        text += ' ' * (lcd_columns - len(text))
        lcd.message = text
            
        while not (lcd.down_button or lcd.left_button or lcd.right_button or lcd.select_button):
            pass
        
        if lcd.left_button:
            self.wifi_add_to_menu_wifi()
            
        if lcd.down_button:
            self.wifi_add_to_delete()
            
        if lcd.right_button or lcd.select_button:
            self.wifi_add_to_choose_wifi()
            
    def on_enter_wifi_delete(self):
        lcd.cursor_position(column=0, row=1)
        text = '>DELETE'
        text += ' ' * (lcd_columns - len(text))
        lcd.message = text
        
        while not (lcd.up_button or lcd.left_button or lcd.right_button or lcd.select_button):
            pass
        
        if lcd.left_button:
            self.wifi_delete_to_menu_wifi()
            
        if lcd.up_button:
            self.wifi_delete_to_add()
        
        if lcd.right_button or lcd.select_button:
            self.wifi_delete_to_delete_wifi()
            
    def on_enter_choose_wifi(self):
        
        lcd.clear()
        lcd.cursor_position(column=0, row=0)
        lcd.message = 'SCANNING...'
        
        wifis = scanWifis()
        
        if len(wifis) == 0:
            lcd.clear()
            lcd.cursor_position(column=0, row=0)
            text = 'NO WIFI\nFOUND...'
            lcd.message = text
            time.sleep(2)
            self.choose_wifi_to_wifi_add()
            
        lcd.clear()
        lcd.cursor_position(column=0, row=0)
        text = 'CHOOSE WIFI:'
        lcd.message = text
            
        i = 0
        
        while True:
            lcd.cursor_position(column=0, row=1)
            text = '>' + decodeName(wifis[i])
            text += ' ' * (lcd_columns - len(text))
            lcd.message = text
            
            while True:
                
                if (i > 0) and lcd.up_button:
                    i -= 1
                    break
                
                if (i < len(wifis) - 1) and lcd.down_button:
                    i += 1
                    break
                
                if lcd.select_button or lcd.left_button or lcd.right_button:
                    break
                
            if lcd.select_button or lcd.left_button or lcd.right_button:
                break
            
        if lcd.left_button:
            self.choose_wifi_to_wifi_add()
            
        if lcd.select_button or lcd.right_button:
            self.ssid = wifis[i]
            self.choose_wifi_to_password_wifi()
                
            
            
    def on_enter_password_wifi(self):
        lcd.clear()
        lcd.cursor_position(column=0, row=0)
        text = 'PASSWORD:'
        lcd.message = text
        
        password_codes = [0 for _ in range(lcd_columns)]
        
        cursor = 0
        lcd.cursor = True
        
        lcd.cursor_position(cursor, 1)
        
        while True:
            while True:
                begin_press = True
                while lcd.up_button:
                    password_codes[cursor] = password_codes[cursor] + 1
                    password_codes[cursor] %= len(letters)
                    lcd.cursor_position(column=cursor, row=1)
                    lcd.message = letters[password_codes[cursor]]
                    lcd.cursor_position(column=cursor, row=1)
                    
                    if begin_press:
                        time.sleep(0.2)
                        begin_press = False
                    else:
                        time.sleep(0.05)
                    
                    
                while lcd.down_button:
                    password_codes[cursor] = password_codes[cursor] - 1
                    password_codes[cursor] %= len(letters)
                    lcd.cursor_position(column=cursor, row=1)
                    lcd.message = letters[password_codes[cursor]]
                    lcd.cursor_position(column=cursor, row=1)
                    
                    if begin_press:
                        time.sleep(0.2)
                        begin_press = False
                    else:
                        time.sleep(0.05)
                        
                if lcd.left_button and (cursor > 0):
                    cursor -= 1
                    lcd.cursor_position(cursor, 1)
                    time.sleep(0.3)
                    break
                
                if lcd.right_button and (cursor < lcd_columns - 1):
                    cursor += 1
                    lcd.cursor_position(cursor, 1)
                    time.sleep(0.3)
                    break
                    
                if lcd.select_button:
                    break
                
            if lcd.select_button:
                self.password = ''.join([letters[code] for code in password_codes]).strip()
                break
                
        lcd.cursor = False
        
        lcd.clear()
        lcd.cursor_position(0, 0)
        lcd.message = 'CONNECTING...'
        time.sleep(0.75)
        
        connected = connectWifi(self.ssid, self.password)
        
        
        if connected:
            lcd.clear()
            lcd.cursor_position(0, 0)
            lcd.message = 'PASSWORD OK'
            time.sleep(1)
            self.password_wifi_to_home()
        else:
            
            lcd.clear()
            lcd.cursor_position(0, 0)
            lcd.message = 'PASSWORD WRONG'
            time.sleep(1)
            self.password_wifi_to_home()
        
        
            
                    
                    
                        
                    
    def on_enter_delete_wifi(self):
        wifis = knownWifis()
        
        if len(wifis) == 0:
            lcd.clear()
            lcd.cursor_position(column=0, row=0)
            text = 'NO WIFI\nSTORED...'
            lcd.message = text
            time.sleep(2)
            self.delete_wifi_to_wifi_delete()
            
        lcd.clear()
        lcd.cursor_position(column=0, row=0)
        text = 'DELETE WIFI:'
        lcd.message = text
            
        i = 0
        
        while True:
            lcd.cursor_position(column=0, row=1)
            text = '>' + decodeName(wifis[i])
            text += ' ' * (lcd_columns - len(text))
            lcd.message = text
            
            while True:
                
                if (i > 0) and lcd.up_button:
                    i -= 1
                    break
                
                if (i < len(wifis) - 1) and lcd.down_button:
                    i += 1
                    break
                
                if lcd.select_button or lcd.left_button or lcd.right_button:
                    break
                
            if lcd.select_button or lcd.left_button or lcd.right_button:
                break
            
        if lcd.left_button:
            self.delete_wifi_to_wifi_delete()
            
        if lcd.select_button or lcd.right_button:
            deleteWifi(wifis[i])
            lcd.clear()
            lcd.cursor_position(column=0, row=0)
            text = 'DELETED:\n' + wifis[i]
            lcd.message = text
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
