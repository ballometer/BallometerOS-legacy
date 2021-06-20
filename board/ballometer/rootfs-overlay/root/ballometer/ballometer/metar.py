import requests
import json

def get_metar(station_id='LSZH'):
    url = f'https://api.ballometer.io/weather/metar?station_id={station_id}'
    try:
        r = requests.get(url, timeout=0.5)
        if r.status_code != 200:
            return {}
        data = json.loads(r.text)
        return {
            'press': float(data['press']),
            'station_id': str(data['station_id']),
            'time': float(data['time']),
        }
    except requests.exceptions.ConnectTimeout:
        return {}
    except json.decoder.JSONDecodeError:
        return {}
    except KeyError:
        return {}
    except TypeError:
        return {}

if __name__ == '__main__':
    print(get_metar('LSGG'))
