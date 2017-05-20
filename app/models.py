# -*- coding: utf-8 -*-
from __init__ import db
from datetime import datetime


class Douban(db.Document):
    meta = {
        'collection': 'DoubanItem',
        'ordering': ['-add_time'],
        'strict': False,
    }
    title = db.StringField()
    content = db.StringField()
    message_url = db.StringField()
    id = db.StringField()
    image_url = db.StringField()
    source_from = db.StringField()
    add_time = db.DateTimeField(default=datetime.utcnow)


    def to_json(self):
        json_douban = {
            'title': self.title,
            'content': self.content,
            'message_url': self.message_url,
            'image_url': self.image_url,
            'source_from': self.source_from

        }
        return json_douban

class Guoke(db.Document):
    meta = {
        'collection': 'GuokeItem',
        'ordering': ['-add_time'],
        'strict': False,
    }
    title = db.StringField()
    content = db.StringField()
    message_url = db.StringField()
    id = db.StringField()
    image_url = db.StringField()
    source_from = db.StringField()
    add_time = db.DateTimeField(default=datetime.utcnow)


    def to_json(self):
        json_douban = {
            'title': self.title,
            'content': self.content,
            'message_url': self.message_url,
            'image_url': self.image_url,
            'source_from': self.source_from

        }
        return json_douban

