import sqlite3
import string
from random import choices
from datetime import datetime
from flask import request
from db import db

class LinkModel(db.Model):
    __tablename__ = 'Links'
    id = db.Column(db.Integer, primary_key=True)
    origin_link = db.Column(db.String(512))
    short_link = db.Column(db.String(4), unique=True)
    created_date = db.Column(db.DateTime, default=datetime.now)
    link_expiration = db.Column(db.Integer, default = 90)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_link = self.gen_short_link()

    def gen_short_link(self):   
        symbols = string.digits + string.ascii_letters
        short_link = ''.join(choices(symbols, k=4))

        link = self.query.filter_by(short_link=short_link).first() # uniqueness checking

        if link:    # if short URL already exist, generating new one
            return self.gen_short_link()
        
        return (short_link)

