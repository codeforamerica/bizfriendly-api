import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.restless
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.admin import Admin
from flask.ext.heroku import Heroku
from flask import request, redirect
import foursquare_lesson

#----------------------------------------
# initialization
#----------------------------------------

app = Flask(__name__)
heroku = Heroku(app) # Sets CONFIG automagically

app.config.update(
	DEBUG = True,
	SQLALCHEMY_DATABASE_URI = 'postgres://hackyourcity@localhost/howtocity',
    SECRET_KEY = '123456'
)

# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)

def add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

app.after_request(add_cors_header)

# import oauth_logins

#----------------------------------------
# models
#----------------------------------------

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    description = db.Column(db.Unicode)
    url = db.Column(db.Unicode)

    def __init__(self, name=None, description=None, url=None):
        self.name = name
        self.description = description
        self.url = url

    def __repr__(self):
        return self.name

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    description = db.Column(db.Unicode)
    url = db.Column(db.Unicode)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('lessons', lazy='dynamic'))

    def __init__(self, name=None, description=None, url=None, category=None):
        self.name = name
        self.description = description
        self.url = url
        self.category = category

    def __repr__(self):
        return self.name

class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    description = db.Column(db.Unicode)
    url = db.Column(db.Unicode)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    lesson = db.relationship('Lesson', backref=db.backref('steps', lazy='dynamic'))
    step_text = db.Column(db.Unicode)
    trigger_endpoint = db.Column(db.Unicode)
    trigger_check = db.Column(db.Unicode)
    trigger_value = db.Column(db.Unicode)
    feedback = db.Column(db.Unicode)
    next_step = db.Column(db.Unicode)

    def __init__(self, name=None, description=None, url=None, lesson=None, step_text=None, trigger_endpoint=None, trigger_check=None, trigger_value=None, feedback=None, next_step=None):
        self.name = name
        self.description = description
        self.url = url
        self.lesson = lesson
        self.step_text = step_text
        self.trigger_endpoint = trigger_endpoint
        self.trigger_check = trigger_check
        self.trigger_value = trigger_value
        self.feedback = feedback
        self.next_step = next_step

    def __repr__(self):
        return self.name

# API ------------------------------------------------------------
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Category, methods=['GET', 'POST', 'DELETE'], url_prefix='/api/v1', collection_name='categories')
manager.create_api(Lesson, methods=['GET', 'POST', 'DELETE'], url_prefix='/api/v1', collection_name='lessons')
manager.create_api(Step, methods=['GET', 'POST', 'DELETE'], url_prefix='/api/v1', collection_name='steps')

# ADMIN ------------------------------------------------------------
admin = Admin(app, name='How to City', url='/api/admin')

class CategoryView(ModelView):
    column_display_pk = True

class LessonView(ModelView):
    column_display_pk = True
    column_auto_select_related = True

class StepView(ModelView):
	column_display_pk = True
	column_auto_select_related = True

admin.add_view(CategoryView(Category, db.session))
admin.add_view(LessonView(Lesson, db.session))
admin.add_view(StepView(Step, db.session))

# Foursquare ------------------------------------------------------------

@app.route('/foursquare/login')
def foursquare_login():
    foursquare_auth_url = foursquare_lesson.foursquare_oauth()
    return redirect(foursquare_auth_url)

@app.route('/foursquare/code')
def foursquare_code():
    auth_code = request.args['code']
    access_token = foursquare_lesson.get_access_token(auth_code)
    return 'WHAT' #'<script>window.close()</script>'

@app.route('/foursquare/loggedin/<access_token>')
def foursquare_loggedin(access_token):
    user = foursquare_lesson.get_user_data(access_token)
    if user:
        return '{"loggedIn":true}'
    else:
        return '{"loggedIn":false}'