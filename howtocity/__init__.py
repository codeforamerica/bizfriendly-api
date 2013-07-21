from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.restless
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.admin import Admin
from flask.ext.heroku import Heroku
from flask import request, redirect
import os, requests, json
#----------------------------------------
# initialization
#----------------------------------------

app = Flask(__name__)
heroku = Heroku(app) # Sets CONFIG automagically

app.config.update(
    # DEBUG = True,
    # SQLALCHEMY_DATABASE_URI = 'postgres://hackyourcity@localhost/howtocity',
    # SECRET_KEY = '123456'
)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)

@app.after_request
def add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

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
    step_type = db.Column(db.Unicode)
    url = db.Column(db.Unicode)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    lesson = db.relationship('Lesson', backref=db.backref('steps', lazy='dynamic'))
    step_text = db.Column(db.Unicode)
    trigger_endpoint = db.Column(db.Unicode)
    trigger_check = db.Column(db.Unicode)
    trigger_value = db.Column(db.Unicode)
    thing_to_remember = db.Column(db.Unicode)
    feedback = db.Column(db.Unicode)
    next_step = db.Column(db.Unicode)

    def __init__(self, name=None, step_type=None, url=None, lesson=None, step_text=None, trigger_endpoint=None, trigger_check=None, trigger_value=None, thing_to_remember=None, feedback=None, next_step=None):
        self.name = name
        self.description = description
        self.url = url
        self.step_type = step_type
        self.step_text = step_text
        self.trigger_endpoint = trigger_endpoint
        self.trigger_check = trigger_check
        self.trigger_value = trigger_value
        self.thing_to_remember = thing_to_remember
        self.feedback = feedback
        self.next_step = next_step

    def __repr__(self):
        return self.name

class Thing_to_remember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.Unicode)
    thing_to_remember = db.Column(db.Unicode)

    def __init__(self, access_token=None, thing_to_remember=None):
        self.access_token = access_token
        self.thing_to_remember = thing_to_remember

    def __repr__(self):
        return self.thing_to_remember

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

# Functions --------------------------------------------------------

@app.route('/logged_in', methods=['POST'])
def logged_in():
    # Check if the user is logged into the service
    access_token = request.args['access_token']
    trigger_endpoint = request.form['triggerEndpoint']
    r = requests.get(trigger_endpoint+access_token)
    rjson = r.json()
    trigger_check = request.form['triggerCheck'].split(',')
    trigger_value = request.form['triggerValue']
    count = 0
    while count < len(trigger_check):
        rjson = rjson[trigger_check[count]]
        count = count + 1
    variableType = type(rjson).__name__
    try:
        trigger_value = eval(variableType+'('+trigger_value+')')
    except TypeError:
        pass
    if rjson == trigger_value:
        return '{"loggedIn":true}'
    return '{"loggedIn":false}'

@app.route('/check_for_new', methods=['POST'])
def check_for_new():
    trigger = False
    original_count = 0
    original_count_flag = False
    # Loop until a new page appears
    while not trigger:
        access_token = request.args['access_token']
        trigger_endpoint = request.form['triggerEndpoint']
        r = requests.get(trigger_endpoint+access_token)
        rjson = r.json()
        trigger_check = request.form['triggerCheck'].split(',')
        trigger_value_endpoint = request.form['triggerValue'].split(',')
        thing_to_remember_endpoint = request.form['thingToRemember'].split(',')
        count = 0
        while count < len(trigger_check):
            rjson = rjson[trigger_check[count]]
            count = count + 1
        assert isinstance(rjson, list)
        if not original_count_flag:
            original_count = len(rjson)
            original_count_flag = True
        if len(rjson) > original_count:
            while count < len(trigger_check):
                rjson = rjson[trigger_check[count]]
                count = count + 1
            trigger = True

    # The new thing should be the last in the list
    the_new_thing = rjson.pop()

    def get_data_at_endpoint(json_data, endpoint_list):
        count = 0
        while count < len(endpoint_list):
            json_data = json_data[endpoint_list[count]]
            count = count + 1
        data = json_data # Should be a string or int now, not json
        return data

    # Save the thing_to_remember in the database
    thing_to_remember = get_data_at_endpoint(rjson, thing_to_remember_endpoint)
    thing_to_remember_db = Thing_to_remember(access_token,thing_to_remember)
    db.session.add(thing_to_remember_db)
    db.session.commit()

    # Return the value at the trigger_value endpoint
    new_thing_name = get_data_at_endpoint(rjson, trigger_value_endpoint)
    return '{"newThingName":"'+new_thing_name+'"}'























