# -*- coding: utf-8 -*-

import os
import requests
import time
from datetime import datetime
import pytz

from datasources.sources import AtomSource, RssSource, TwitterSource

# Contants
BOT_ID = 'YOUR-BOT-ID-HERE'
BOT_URL = u"http://api.telegram.org/bot%s/sendMessage" % BOT_ID
BOT_CHANNEL = "@HackLabAlmeria_novedades"
GROUP_ID = '-158329500'
LAST_ITEM_PATH = 'last_item'

# Config
PARSE_ONLY_NEW = True
SOURCES = [
#    AtomSource('http://hacklabalmeria.net/atom.xml'),
#    RssSource('https://foro.hacklabalmeria.net/c/observatorio.rss'),
    RssSource('https://foro.hacklabalmeria.net/latest.rss'),
    TwitterSource('https://twitrss.me/twitter_user_to_rss/?user=hacklabal')
]

# Properties
lastItemFile = None
lastParsedDate = None

if PARSE_ONLY_NEW:
    if os.path.isfile(LAST_ITEM_PATH):
        lastItemFile = open(LAST_ITEM_PATH, 'r+')

    if lastItemFile:
        contents = lastItemFile.readline()
        if contents:
            lastParsedDate = datetime.fromtimestamp(float(contents))
            lastParsedDate = lastParsedDate.replace(tzinfo=pytz.UTC)
        lastItemFile.seek(0)
    else:
        lastItemFile = open(LAST_ITEM_PATH, 'w')

messages = []

for source in SOURCES:
    # Parse and merge all messages
    messages += filter(None, source.parse(lastParsedDate))

# Sort by date ASC
sortedMessages = sorted(messages, key=lambda message: message.date)

# Send all messages to channel
# TODO Add 'Senders'
# TODO Maybe add a delay?
botHttpRequest = requests.Session()
for message in sortedMessages:
    url = BOT_URL

    # Send to Channel
    postBody = { 'chat_id' : BOT_CHANNEL,
                 'text' : message.text,
                 'parse_mode' : 'HTML'}

    botHttpRequest.request(url=url, method='POST', data=postBody)

    # Send to group
    postBody = {'chat_id': GROUP_ID,
                'text': message.text,
                'parse_mode': 'HTML'}

    response = botHttpRequest.request(url=url, method='POST', data=postBody)

    if response.status_code == 400:
        print(u"Error (%s) on message: \n%s\n\n" % (response.text, message.text))
    else:
        # Only save date from the last message that was sent correctly
        lastParsedDate = message.date
        print(str(response.status_code) + u": " + response.text)

if lastParsedDate:
    lastItemFile.write(str(time.mktime(lastParsedDate.utctimetuple())))

lastItemFile.close()
