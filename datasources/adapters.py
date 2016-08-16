# -*- coding: utf-8 -*-

from models import Message
from dateutil import parser
import re

class Adapter:
    def convertItem(self, item, minDate = None):
        pass

    def cleanTag(self, text, removeAllTags = False):
        # Apparently, Telegram doesn't allow <a> with empty hrefs
        text = re.sub(r'<a href="">(.*?)</a>', r'\1', text)

        # Telegram only accepts a few HTML tags - and not nested tags -
        # so we may have to remove all existing tags to ensure compatibility
        if removeAllTags:
            text = re.sub(r'<.*?>(.*?)</.*?>', r'\1', text)
            text = text.replace('<', '&lt;')
            text = text.replace('>', '&gt;')
            text = text.replace('&', '&amp;')
        else:
            # <strong> should be <b>
            text = text.replace("<strong>", "<b>")
            text = text.replace("</strong>", "</b>")
        return text

class AtomAdapter(Adapter):
    def convertItem(self, item, minDate = None):

        date = parser.parse(item.updated.string)

        # Check if needs to parse
        if minDate and minDate >= date:
            return

        title = item.title.string.strip()

        lugar = None
        fecha = None

        lugarRegex = re.findall(r'<p>Lugar: (.*?)</p>', item.content.string)
        if len(lugarRegex) > 0:
            lugar = self.cleanTag(lugarRegex[0], removeAllTags=True)

        fechaRegex = re.findall(r'<p>Fecha: (.*?)</p>\s<p>Hora: (.*?)</p>', item.content.string)
        if len(fechaRegex) > 0 and len(fechaRegex[0]) > 1:
            fecha = u'' + self.cleanTag(fechaRegex[0][0] + u", " + fechaRegex[0][1], removeAllTags=True)

        url = item.link['href'].encode('utf8')

        text = u'<b>Evento:</b> %s\n' % (title)

        if lugar:
            text += u'<b>Lugar:</b> %s\n' % lugar

        if fecha:
            text += u'<b>Fecha y hora:</b> %s\n' % fecha

        text += u'<b>Más info:</b> <a href="%s">%s</a> ' % (url, url)

        message = Message()
        message.text = text
        message.date = date

        return message

class RssAdapter(Adapter):
    def convertItem(self, item, minDate):

        date = parser.parse(item.pubDate.string)

        # Check if needs to parse
        if minDate and minDate >= date:
            return

        title = self.cleanTag(item.title.string.strip(), removeAllTags=True)
        category = item.category.string
        author = item.find(name='creator', text=False).string
        url = item.link.string

        text = u'<b>%s</b> ha creado un nuevo tema en <i>%s: </i><b>%s</b> \n<a href="%s">%s</a>' \
               % (author, category, title, url, url)

        message = Message()
        message.text = text
        message.date = date

        return message

class TwitterAdapter(Adapter):
    def convertItem(self, item, minDate):

        date = parser.parse(item.pubDate.string)

        # Check if needs to parse
        if minDate and minDate >= date:
            return

        message = self.cleanTag(item.title.string)
        author = item.find(name='creator', text=False).string
        url = item.link.string

        text = u'<b>%s:</b> %s \n\n<a href="%s">%s</a>' \
               % (author, message, url, url)

        message = Message()
        message.text = text
        message.date = date

        return message