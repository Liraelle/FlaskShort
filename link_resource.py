import sqlite3
import datetime
from flask_restful import Resource, reqparse
from flask import redirect, request
from link_model import LinkModel
from db import db

_link_parser = reqparse.RequestParser()
_link_parser.add_argument('URL', 
                    type = str, 
                    required = True, 
                    help = "Paste your link here.")
_link_parser.add_argument('URL_expiration', 
                    type = int, 
                    required = False, 
                    help = "You can specify how many days link can live.")

# getting original URL from user
class Link(Resource):   
    def get(self):
        link = _link_parser.parse_args()
        
        if link['URL_expiration'] < 1 or link['URL_expiration'] > 365:
            return {'message': 'Incorrect value. It should be number from 1 to 365.'}

        counting = LinkModel.query.count()

# creating new short URL if in database less than 1 million URL 
        if counting < 1000000:  
            if link['URL_expiration']:
                exp_date = datetime.date.today() + datetime.timedelta(days=link['URL_expiration'])
                item = LinkModel(link['URL'], exp_date) # creating short URL with custom lifetime
            else:
                exp_date = datetime.date.today() + datetime.timedelta(days=90)
                item = LinkModel(link['URL'], exp_date) # creating short URL with standart lifetime

            item.save_to_db()

            return {'short_link': request.base_url+item.short_link,
                        'count': counting}

# if in database 1 million URL before creating new one, serching expired URl and deleting it
        if counting >= 1000000: 
            exp_url = LinkModel.query.filter(LinkModel.link_expiration < datetime.date.today()).first()
            if exp_url:
                exp_url.delete_expired()

                if link['URL_expiration']:
                    exp_date = datetime.date.today() + datetime.timedelta(days=link['URL_expiration'])
                    item = LinkModel(link['URL'], exp_date) # creating short URL
                else:
                    exp_date = datetime.date.today() + datetime.timedelta(days=90)
                    item = LinkModel(link['URL'], exp_date) # creating short URL

                item.save_to_db()

                return {'short_link': request.base_url+item.short_link,
                        'count': counting}

# if in database 1 million active URL 
        return {'message': 'Database  is full'}


# redirecting from short URL to original
class Short_link(Resource): 
    def get(self, short_link):
        link = LinkModel.find_link(short_link)
        if link.link_expiration < datetime.datetime.today():   # deleting URL if expired
            link.delete_expired()
            return {'message': 'URL expired.'}

        return redirect(link.origin_link)   # redirecting to original URL
