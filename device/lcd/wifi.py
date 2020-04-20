import time
import subprocess
import re
import codecs

def decodeName(name):
    def match_function(matchobj):
        snippet = matchobj.group(0)
        hex_1 = snippet[2:4]
        hex_2 = snippet[6:8]
        hex_3 = ''
        if len(snippet) == 12:
            hex_3 = snippet[10:12]

        return codecs.decode(hex_1 + hex_2 + hex_3, 'hex').decode('utf-8')

    return re.sub(r'(\\x[0-9a-fA-F]{2}){2,3}', match_function, name)

def getIP():
    ip = ''
    
    lines = subprocess.run(['ifconfig', 'wlan0'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    
    m = re.search('inet (\S*) ', lines)
    
    if m != None:
        ip = m.group(0)[5:].strip()
        
    return ip

def knownWifis():
    wifis = []

    lines = []
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r') as f:
        lines = f.read().splitlines()
    
    for line in lines:
        if 'ssid' in line:
            wifis.append(line.strip()[7:-1])
            
    

    return wifis


def deleteWifi(ssid):
    lines = []
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r') as f:
        lines = f.read().splitlines()
    
    for i in range(len(lines)):
        if ssid in lines[i]:
            del lines[(i - 1):(i + 3)]
            break

    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as f:
        for line in lines:
            f.write(line + '\n')
        f.close()

    try:
        result = subprocess.run(['wpa_cli', '-i', 'wlan0', 'reconfigure'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    except:
        print('wpa_cli did not work')


def scanWifis():
    wifis = []
    result = ''
    try:
        result = subprocess.run(['iwlist', 'wlan0', 'scan'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    except:
        print('iwlist did not work')

    lines = result.splitlines()
    for line in lines:
        line = line.strip()
        if 'ESSID' in line:
            ssid = line[7:-1]
            if ssid != '':
                wifis.append(ssid)

    return wifis

def connectWifi(ssid, password):
    success = False

    deleteWifi(ssid)
    
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'a') as f:
        lines = []
        lines.append('network={')
        lines.append('\tssid=P"' + ssid + '"')
        lines.append('\tpsk="' + password + '"')
        lines.append('}')

        for line in lines:
            f.write(line + '\n')

        f.close()

    result = ''
    try:
        result = subprocess.run(['wpa_cli', '-i', 'wlan0', 'reconfigure'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    except:
        print('wpa_cli did not work')

    if 'OK' in result:
        success = True
    else:
        success = False

    if not success:
        deleteWifi(ssid)

    return success

