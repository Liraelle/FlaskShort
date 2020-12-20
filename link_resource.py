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

class Link(Resource):   # getting original URL from user
    def get(self):
        link = _link_parser.parse_args()
        
        counting = LinkModel.query.count()
        if counting < 15:
            if link['URL_expiration']:
                #exp_date = datetime.date.today() + datetime.timedelta(days=link['URL_expiration'])
                exp_date = datetime.date(2020, 4, 12) + datetime.timedelta(days=link['URL_expiration'])
                item = LinkModel(link['URL'], exp_date) # creating short URL
            else:
                #exp_date = datetime.date.today() + datetime.timedelta(days=90)
                exp_date = datetime.date(2020, 4, 12) + datetime.timedelta(days=90)
                item = LinkModel(link['URL'], exp_date) # creating short URL

            item.save_to_db()

            return {'short_link': request.base_url+item.short_link,
                        'count': counting}
        return {'message': 'database  is full'}


class Short_link(Resource): # redirecting from short URL to original
    def get(self, short_link):
        url = LinkModel.find_link(short_link)

        return redirect(url.origin_link)
