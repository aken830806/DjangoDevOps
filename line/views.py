import requests


def push_notify_text_message(access_token, message):
    return requests.post('https://notify-api.line.me/api/notify', params={'message': message},
                         headers={'Authorization': 'Bearer ' + access_token,
                                  'Content-Type': 'application/x-www-form-urlencoded'})


def get_token_status(access_token):
    headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.get('https://notify-api.line.me/api/status', headers=headers).json()
