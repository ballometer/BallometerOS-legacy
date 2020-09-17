import time
import subprocess
import re
import codecs

path_wpa_supplicant = '/etc/wpa_supplicant.conf'

class WiFi:
    def decode_name(self, name):
        def match_function(matchobj):
            snippet = matchobj.group(0)
            hex_1 = snippet[2:4]
            hex_2 = snippet[6:8]
            hex_3 = ''
            if len(snippet) == 12:
                hex_3 = snippet[10:12]

            return codecs.decode(hex_1 + hex_2 + hex_3, 'hex').decode('utf-8')

        return re.sub(r'(\\x[0-9a-fA-F]{2}){2,3}', match_function, name)

    def get_ip(self):
        ip = ''
        
        lines = subprocess.run(['ifconfig', 'wlan0'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        
        m = re.search('inet (\S*) ', lines)
        
        if m != None:
            ip = m.group(0)[10:].strip()
            
        return ip

    def known(self):
        wifis = []

        lines = []
        with open(path_wpa_supplicant, 'r') as f:
            lines = f.read().splitlines()
        
        for line in lines:
            if 'ssid' in line:
                result = re.search('"(.*)"', line)
                if hasattr(result, 'group'):
                    wifis.append(result.group(1))  

        return wifis


    def remove(self, ssid):
        lines = []
        with open(path_wpa_supplicant, 'r') as f:
            lines = f.read().splitlines()
        
        for i in range(len(lines)):
            if ssid in lines[i]:
                del lines[(i - 1):(i + 3)]
                break

        with open(path_wpa_supplicant, 'w') as f:
            for line in lines:
                f.write(line + '\n')
            f.close()

        try:
            subprocess.run(['wpa_cli', '-i', 'wlan0', 'reconfigure'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        except:
            print('wpa_cli did not work')


    def scan(self):
        wifis = []

        attempts = 0
        while attempts < 10:
            attempts += 1
            result = subprocess.run(['wpa_cli', '-i', 'wlan0', 'scan'], stdout=subprocess.PIPE).stdout.decode('utf-8')
            if 'OK' in result:
                break
            time.sleep(1)
            
        if 'FAIL-BUSY' in result:
            return []
        
        result = subprocess.run(['wpa_cli', '-i', 'wlan0', 'scan_results'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        
        lines = result.splitlines()
        
        for line in lines:
            tab_index = line.rfind('\t')
            if tab_index > 0:
                ssid = line[tab_index:].strip()
                if ssid != '' and ssid not in wifis:
                    wifis.append(ssid)
        return wifis

    def add(self, ssid, password):
    
        self.remove(ssid)
        
        with open(path_wpa_supplicant, 'a') as f:
            lines = []
            lines.append('network={')
            lines.append('\tssid=P"' + ssid + '"')
            lines.append('\tpsk="' + password + '"')
            lines.append('}')

            for line in lines:
                f.write(line + '\n')

            f.close()

        subprocess.run(['wpa_cli', '-i', 'wlan0', 'reconfigure'], stdout=subprocess.PIPE).stdout.decode('utf-8')
