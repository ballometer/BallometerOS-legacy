import RPi.GPIO as GPIO
import time
import numpy as np
from scipy.interpolate import interp1d

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN)

def detect_start(timeout, invert=False):   
    
    t_initial = time.time()
    t_min = 1.9 * 1038 * 1e-6
    t_max = 2.1 * 1038 * 1e-6
        
    while time.time() - t_initial < timeout:
        tic = time.time()
        if invert:
            GPIO.wait_for_edge(4, GPIO.FALLING)
        else:
            GPIO.wait_for_edge(4, GPIO.RISING)
            
        toc = time.time()
        
        if ((toc - tic) < t_min) or (t_max < (toc - tic)):
            continue
        
        tic = time.time()
        if invert:
            GPIO.wait_for_edge(4, GPIO.FALLING)
        else:
            GPIO.wait_for_edge(4, GPIO.RISING)
        toc = time.time()
        
        if ((toc - tic) < t_min) or (t_max < (toc - tic)):
            continue
        
        cycles = 0
        
        while time.time() - t_initial < timeout:
            cycles += 1
            
            tic = time.time()
            if invert:
                GPIO.wait_for_edge(4, GPIO.FALLING)
            else:
                GPIO.wait_for_edge(4, GPIO.RISING)
            toc = time.time()
       
            if (toc - tic) < t_max:
                continue
            else:
                break
            
        if cycles < 10:
            break
    
    if time.time() - t_initial >= timeout:
        return -1.0
    else:
        return tic
    
def parse_temperature(shift, data):
    result = 0.0
       
    result += 1.0 * ((int(data[0 + shift]) << 0) + (int(data[1 + shift]) << 1) + (int(data[2 + shift]) << 2) + (int(data[3 + shift]) << 3))

    return result
    
def measure(timeout=10, invert=False):
    start_time = detect_start(timeout, invert)
    
    if start_time < 0:
        return None, None
    
    toc = time.time()
    
    if toc - start_time > 50 * 1e-3:
        return None, None
    
    N = 50
    t = np.zeros(N)
    state4 = np.zeros(N)

    i = 0
    last_state = 1
    
    t[i] = time.time()
    state4[i] = last_state
    
    i += 1

    while i < N:
        if last_state == 0:
            if invert:
                GPIO.wait_for_edge(4, GPIO.FALLING)
            else:
                GPIO.wait_for_edge(4, GPIO.RISING)
            last_state = 1
        else:
            if invert:
                GPIO.wait_for_edge(4, GPIO.RISING)
            else:
                GPIO.wait_for_edge(4, GPIO.FALLING)
            last_state = 0
        
        state4[i] = last_state
        t[i] = time.time()
        
        if 51 * 1e-3 < t[i] - start_time:
            t = t[0:i]
            state4 = state4[0:i]
            break
        
        i += 1
        
    t -= start_time
            
    t = np.append([0], t)
    state4 = np.append([0], state4)
    
    
    t_sample = np.arange(1038 * 1e-6 / 2, t[-1] - 2 * 1e-3, 1038 * 1e-6)
    f_1 = interp1d(t, state4, kind='previous')
    state_sample = f_1(t_sample)
    
    i = 22
    
    if len(state_sample) < i + 4 + 2 + 4 + 4 + 4:
        return None, None
    
    result = 0
    result += 0.1 * parse_temperature(shift=i, data=state_sample)
    result += 1.0 * parse_temperature(shift=i + 4, data=state_sample)
    result += 10.0 * parse_temperature(shift=i + 4 + 2 + 4, data=state_sample)
    result += 100.0 * parse_temperature(shift=i + 4 + 2 + 4 + 4, data=state_sample)
    
    if result > 155:
        return None, None
        
    s = ''
    for x in state_sample:
        s += str(int(x))

    return (result, int(s[0:22], 2))

if __name__ == '__main__':
    setup()
    
    while True:
        tic = time.time()
        temperature, address = measure(timeout=10, invert=True)
        print('%1.1f s' % (time.time() - tic))
        if temperature == None:
            print('none')
            print('')
        else:
            print('%1.1f deg C' % temperature)
            print(address)
            print('')
            
