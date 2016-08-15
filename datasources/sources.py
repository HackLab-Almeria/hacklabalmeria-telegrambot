# -*- coding: utf-8 -*-

from adapters import AtomAdapter, RssAdapter, TwitterAdapter
from bs4 import BeautifulSoup
import requests

class Source:

    url = None
    adapter = None

    def __init__(self, url):
        if url is None:
            raise "Can't crate a Source with an empty url"
        else:
            self.url = url

    def parse(self, minDate = None):

        if self.url is None:
            raise "Must add an URL to parse"

        items = self.loadFromURL(self.url)
        messages = self.parseItemToMessages(items, minDate)
        return messages

    def loadFromURL(self, url):
        pass

    def parseItemToMessages(self, items, minDate = None):
        messages = []

        for item in items:
            message = self.adapter.convertItem(item, minDate)
            messages.append(message)

        return messages


class AtomSource(Source):

    adapter = AtomAdapter()

    def loadFromURL(self, url):
        http = requests.Session()
        response = http.request('GET', url)

        if response.status_code == 200 and response.text:
            parser = BeautifulSoup(response.text, 'lxml-xml', from_encoding='utf-8')
            entries = parser.feed.find_all('entry')

            items = []

            for entry in entries:
                items.append(entry)

        else:
            raise "Could not update from URL %" (url)

        return items

class RssSource(Source):

    adapter = RssAdapter()

    def loadFromURL(self, url):
        http = requests.Session()
        response = http.request('GET', url)

        if response.status_code == 200 and response.text:
            parser = BeautifulSoup(response.text, 'lxml-xml', from_encoding='utf-8')
            entries = parser.find_all('item')

            items = []

            for entry in entries:
                items.append(entry)

        else:
            raise "Could not update from URL %" (url)

        return items

class TwitterSource(Source):

    adapter = TwitterAdapter()

    def loadFromURL(self, url):
        http = requests.Session()
        response = http.request('GET', url)

        if response.status_code == 200 and response.text:
            parser = BeautifulSoup(response.text, 'lxml-xml', from_encoding='utf-8')
            entries = parser.find_all('item')

            items = []

            for entry in entries:
                items.append(entry)

        else:
            raise "Could not update from URL %"(url)

        return items