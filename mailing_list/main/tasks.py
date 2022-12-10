import os
import requests

from dotenv import load_dotenv

from mailing_list.celery import app
from .models import Message

load_dotenv()

TOKEN = os.getenv('TOKEN')
URL = os.getenv('URL')
HEADERS = {'Authorization': f'Bearer {TOKEN}',
           'Content-Type': 'application/json'}


@app.task(bind=True, retry_backoff=True)
def send_mails(self, data):
    print(URL)
    try:
        requests.post(
            url=URL + str(data['id']), headers=HEADERS, json=data)
    except requests.exceptions.RequestException as exc:
        raise self.retry(exc=exc)
    else:
        Message.objects.filter(pk=data['id']).update(status='Sent')
