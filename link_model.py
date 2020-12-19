import sqlite3
from db import db

class LinkModel(db.Model):
    __tablename__ = 'Links'
    id = db.Column(db.Integer, primary_key=True)
    origin_link = db.Column(db.String)
    short_link = db.Column(db.String)
    link_expiration = db.Column(db.Datetime(timezone=True))

    def __init__(self, origin_link, short_link):
        self.origin_link = origin_link
        self.short_link = short_link


