import ballometer
import json
import requests
import os
import time


ballometer_url = os.environ.get('BALLOMETER_URL')
if ballometer_url == None:
    ballometer_url = 'https://ballometer.io'

    
store = ballometer.Store()


def get_username_password():
    username = 'default-user-name'
    password = 'default-password'

    try:
        # this file should look like
        # {
        #     "username": "your-username",
        #     "password": "your-password"
        # }
        with open('/data/credentials.json') as f:
            credentials = json.load(f)
            username = credentials['username']
            password = credentials['password']
            
    except json.decoder.JSONDecodeError as e:
        print('json.decoder.JSONDecodeError ' + format(e))
    except FileNotFoundError as e:
        print('FileNotFoundError ' + format(e))
    except KeyError as e:
        print('KeyError ' + format(e))
        
    return username, password


def get_jwt_token(username, password):
    token = ''
    
    body = {
        'username': username,
        'password': password
    }
    
    try:
        r = requests.post(ballometer_url + '/api/auth/login', 
                          json=body, timeout=15)
    except requests.exceptions.ConnectTimeout:
        handle_offline()
        return ''
    
    if r.status_code == 403:
        handle_wrong_credentials(username, password)
        return ''

    try:
        token = r.json()['token']
    except json.decoder.JSONDecodeError:
        return ''
    except KeyError:
        return ''
    
    return token


def handle_wrong_credentials(username, password):
    # Fire some signal flare to the user that the
    # password or username is wrong.
    pass


def handle_offline():
    # Fire some signal flare to the user that the
    # ballometer is offline.
    pass

def handle_400(error):
    # Uploading did not work with status code 400 
    # bad request. Let the user somehow know.
    pass

while True:
    while True:
        username, password = get_username_password()
        token = get_jwt_token(username, password)
        if token == '':
            # 80 percent of all problems solve themselves
            time.sleep(10)
        else:
            break

    while True:
        points = store.get_raw_points(start=store.uploaded_until, limit=100)

        if len(points) == 0:
            # no data to upload
            time.sleep(1)
            continue
        
        try:
            r = requests.post(ballometer_url + '/api/upload/' + username, 
                            json=points,
                            headers={'Authorization': 'Bearer ' + token},
                            timeout=15)
        except requests.exceptions.ConnectTimeout:
            handle_offline()
            time.sleep(10)
            continue
        
        if r.status_code == 403:
            # Forbidden
            # probably the token has expired
            break
        
        if r.status_code == 200:
            store.uploaded_until = points[-1]['time']
        
        if r.status_code == 400:
            # Bad request
            handle_400(r.text)
        
        if time.time() - store.uploaded_until < 5:
            time.sleep(1)
