import sqlite3
from flask_restful import Resource, reqparse
from flask import redirect, request
from link_model import LinkModel
from db import db

_link_parser = reqparse.RequestParser()
_link_parser.add_argument('URL', 
                    type = str, 
                    required = True, 
                    help = "Paste your link here.")
#_link_parser.add_argument('URL_expiration', 
#                    type = int, 
#                    required = False, 
#                    help = "You can specify how many days link can live.")

class Link(Resource):   # getting original URL from user
    def get(self):
        link = _link_parser.parse_args()
        
        #if link['URL_expiration']:
        #    item = LinkModel(origin_link=link['URL'])
        #    item = LinkModel(link_expiration=link['URL_expiration'])
        #else:
        item = LinkModel(origin_link=link['URL'])   # creating short URL

        db.session.add(item)
        db.session.commit()

        return {'short_link': item.short_link}

class Short_link(Resource): #redirecting from short URL to original
    def get(self, short_link):
        url = LinkModel.query.filter_by(short_link=short_link).first_or_404()

        return redirect(url.origin_link)
