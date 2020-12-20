import sqlite3
import string
from random import choices
from datetime import datetime, date, timedelta
from flask import request
from db import db

class LinkModel(db.Model):
    __tablename__ = 'Links'
    id = db.Column(db.Integer, primary_key=True)
    origin_link = db.Column(db.String(512))
    short_link = db.Column(db.String(4), unique=True)
    created_date = db.Column(db.DateTime, default=date(2020, 4, 12))
    #created_date = db.Column(db.DateTime, default=date.today)
    link_expiration = db.Column(db.DateTime)

    def __init__(self, origin_link, link_expiration, **kwargs):
        self.origin_link = origin_link
        self.link_expiration = link_expiration
        self.short_link = self.gen_short_link()

    def gen_short_link(self):   
        symbols = string.digits + string.ascii_letters
        short_link = ''.join(choices(symbols, k=4))

        link = self.query.filter_by(short_link=short_link).first() # uniqueness checking

        if link:    # if short URL already exist, generating new one
            return self.gen_short_link()
        
        return (short_link)


    def save_to_db(self):   # inserting and updating data to database
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_link(cls, short_link):
        return cls.query.filter_by(short_link = short_link).first_or_404()

    @classmethod
    def delete_expired(cls, link_expiration):
        limit = datetime.now() - timedelta(days=link_expiration)
        cls.query.filter(LinkModel.created_date <= limit).delete()
        db.session.commit()
        return {'message'}

