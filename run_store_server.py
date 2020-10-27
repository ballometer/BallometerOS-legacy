import uvicorn
import fastapi
import ballometer
from fastapi.middleware.cors import CORSMiddleware

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


@app.get('/')
def root():
    return '<p>Hello from store. <a href="docs">Docs</a>.</p>'


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
