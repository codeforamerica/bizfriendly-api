from bizfriendly import app
from flask.ext.heroku import Heroku
import os

heroku = Heroku(app) # Sets CONFIG automagically
app.config.update(
    DEBUG = True,
    # SQLALCHEMY_DATABASE_URI = 'postgres://hackyourcity@localhost/howtocity',
    # SQLALCHEMY_DATABASE_URI = 'postgres://postgres:root@localhost/howtocity',
    # SECRET_KEY = '123456'
)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MAIL_GUN_KEY'] = os.environ.get('MAIL_GUN_KEY')
app.config['AWS_ACCESS_KEY_ID'] = os.environ.get('AWS_ACCESS_KEY_ID')
app.config['AWS_SECRET_ACCESS_KEY'] = os.environ.get('AWS_SECRET_ACCESS_KEY')
app.config['S3_BUCKET_NAME'] = os.environ.get('S3_BUCKET_NAME')

def add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, PATCH, DELETE, OPTIONS'
    return response
app.after_request(add_cors_header)