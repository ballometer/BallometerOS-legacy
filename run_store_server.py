import uvicorn
import fastapi
import ballometer
from fastapi.middleware.cors import CORSMiddleware
import time


app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)
store = ballometer.Store()


@app.get('/clock_was_synchronized')
def clock_was_synchronized() -> bool:
    return store.clock_was_synchronized()


@app.get('/get_saved')
def get_saved():
    '''
        Returns for all the keys the last value that was
        saved in the format
        {
            'bmp_pressure': {
                'value': 98443.0,
                'unixtime': 123456.0
            },
            'sht_temperature': {
                'value': 302.1,
                'unixtime': 123456.0
            },
            ...
        }
    '''
    return store.get_saved()


@app.get('/get_history')
def get_history():
    '''
        Returns for the current flight all the measurements that
        were stored using linear interpolation
        [
            {'time': 1605124158.0, 'sht_temperature': 302.1, ...},
            {'time': 1605124159.0, 'sht_temperature': 300.4, ...},
            ...
        ]
    '''
    return store.get_history()


@app.get('/recording')
def recording() -> bool:
    return store.recording


@app.get('/flight_id')
def flight_id() -> int:
    return store.flight_id


@app.get('/qnh')
def qnh() -> int:
    return store.qnh


@app.get('/now')
def get_now():
    '''
        Returns the last measurement of altitude, speed,
        heading, climb, longitude, and latitude:
        {  
            'altitude': 1464.343,
            'speed': 8.6,
            'heading': 234, 
            'climb': 1.6,
            'longitude': 8.43490,
            'latitude': 43.4309
            'time': 1608397940.45
        }
    '''
    result = {}

    point = store.get_saved()

    ui_store_mapping = {
        'altitude': 'vario_altitude',
        'speed': 'gps_speed',
        'heading': 'gps_heading', 
        'climb': 'vario_speed',
        'longitude': 'gps_longitude',
        'latitude': 'gps_latitude'
    }

    for key in ui_store_mapping:
        try:
            result[key] = point[ui_store_mapping[key]]['value']
        except KeyError:
            result[key] = None

    result['time'] = time.time()

    return result

@app.get('/before')
def get_before():
    '''
    Returns the interpolated measurements of the current 
    flight in the form:
    {
        'altitude': [918.8838187009885, 919.222839137572, ...], 
        'speed': [12.3, 13.4, ...],
        'climb': [0.5880960494320139, 0.5206506714967045, ...], 
        'longitude': [8.43490, 8.43491, ...], 
        'latitude': [43.64543, 43.645431, ...], 
        'time': [1608369593.0, 1608369594.0, ...]
    }
    '''
    result = {}

    ui_store_mapping = {
        'altitude': 'vario_altitude',
        'speed': 'gps_speed',
        'heading': 'gps_heading', 
        'climb': 'vario_speed',
        'longitude': 'gps_longitude',
        'latitude': 'gps_latitude',
        'time': 'time'
    }

    for key in ui_store_mapping:
        result[key] = []

    points = store.get_history()

    for point in points:
        for key in ui_store_mapping:
            try:
                result[key].append(point[ui_store_mapping[key]])
            except KeyError:
                result[key].append(None)

    return result


@app.get('/', response_class=fastapi.responses.HTMLResponse)
def root():
    return '<p>Hello from store. <a href="docs">Docs</a>.</p>'


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
