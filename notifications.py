import requests
import logging

def send_push_notification(message: dict, token: str, user: str):
    payload = {"message": message, "token": token, "user": user}
    headers = {'User-Agent': 'Python', "Content-type": "application/x-www-form-urlencoded"}
    r = requests.post(
        'https://api.pushover.net/1/messages.json',
        data=payload, 
        headers=headers
    )
    logging.info(r.status_code)
    logging.info(r.reason)