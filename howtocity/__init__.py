from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku

#----------------------------------------
# initialization
#----------------------------------------

app = Flask(__name__, template_folder='../web/templates', static_folder='../web/static')
heroku = Heroku(app) # Sets CONFIG automagically
db = SQLAlchemy(app)

# app.config.update(
# 	DEBUG = True,
# 	SQLALCHEMY_DATABASE_URI = 'postgres://hackyourcity@localhost/howtocity',
# 	SECRET_KEY = '123456'
# )

import api, web
