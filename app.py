"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask
from flask_restful import  Api
import sqlite3

from db import db
from link_resource import Link, Short_link

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Nata'
api = Api(app)

@app.before_first_request
def create_table():
    db.create_all()


api.add_resource(Link, '/')
api.add_resource(Short_link, '/<string:short_link>')

if __name__ == '__main__':
    db.init_app(app)
    app.run()
