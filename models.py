# -*- coding: utf-8 -*-

class Message:
    text = None
    date = None

    def __repr__(self):
        return self.date.isoformat() + " | " + self.text