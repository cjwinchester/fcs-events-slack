import os
import json
from datetime import date

import requests

today = date.today()
y, m, d = today.year, str(today.month).zfill(2), str(today.day).zfill(2)

url = ('https://www.nrc.gov/reading-rm/doc-collections/'
       'event-status/event/{y}/{y}{m}{d}en.html'.format(y=y, m=m, d=d))

text = 'fort calhoun'

r = requests.get(url)
r.raise_for_status()

if text.casefold() in r.text.casefold():

    slack_hook = os.environ.get('NCC_SLACK_WEBHOOK')

    payload = {
        'channel': '#fcs-alerts',
        'username': 'FCS bot',
        'icon_emoji': ':warning:',
        'text': 'I found a new reportable event at FCS: {}'.format(url)
    }

    payload_as_json = json.dumps(payload)

    if slack_hook:
        requests.post(slack_hook, data=payload_as_json)
    else:
        print('You need the "NCC_SLACK_WEBHOOK" variable.')
