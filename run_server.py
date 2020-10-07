import uvicorn
import fastapi
import ballometer

app = fastapi.FastAPI()
store = ballometer.Store()


@app.get('/get_saved')
def get_saved():
    return store.get_saved()


@app.get('/get_history')
def get_history():
    return store.get_history()


@app.get('/')
def root():
    a = 'a'
    b = 'b' + a
    return {'hello world': b}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
