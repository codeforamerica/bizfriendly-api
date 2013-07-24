from flask import Flask, request, redirect
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.restless
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.admin import Admin
from flask.ext.heroku import Heroku
import os, requests, json, time
#----------------------------------------
# initialization
#----------------------------------------


app = Flask(__name__)
heroku = Heroku(app) # Sets CONFIG automagically

app.config.update(
    # DEBUG = True,
    # SQLALCHEMY_DATABASE_URI = 'postgres://postgres@localhost/howtocity',
    # SECRET_KEY = '123456'
)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)

def add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

app.after_request(add_cors_header)

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

def get_data_at_endpoint(json_data, endpoints):
    for endpoint in endpoints:
        json_data = json_data[endpoint]
    data = json_data # Should be a string or int now, not json
    return data

def boolify(s):
    if s == 'True' or s == 'true':
        return True
    if s == 'False' or s == 'false':
        return False
    raise ValueError("huh?")

def autoconvert(s):
    for fn in (boolify, int, float):
        try:
            return fn(s)
        except ValueError:
            pass
    return s

@app.route('/logged_in', methods=['POST'])
def logged_in():
    # Check if the user is logged into the service
    access_token = request.args['access_token']
    trigger_endpoint = request.form['triggerEndpoint']
    trigger_check_endpoints = request.form['triggerCheck'].split(',')
    trigger_value = request.form['triggerValue']
    counter = 0
    while counter < 60:
        counter = counter + 1
        r = requests.get(trigger_endpoint+access_token)
        rjson = r.json()
        for trigger_check_endpoint in trigger_check_endpoints:
            try:
                rjson = rjson[trigger_check_endpoint]
            except KeyError:
                # return 'The trigger check endpoint is set up wrong.'
                pass
        trigger_value = autoconvert(trigger_value)
        if rjson == trigger_value:
            return '{"loggedIn":true}'
        time.sleep(1)
    return 'TIMEOUT'

@app.route('/check_for_new', methods=['POST'])
def check_for_new():
    access_token = request.args['access_token']
    trigger_endpoint = request.form['triggerEndpoint']
    trigger_check_endpoints = request.form['triggerCheck'].split(',')
    trigger_value_endpoints = request.form['triggerValue'].split(',')
    thing_to_remember_endpoints = request.form['thingToRemember'].split(',')
    trigger = False
    original_count = 10000000
    original_count_flag = False
    timer = 0
    while timer < 60:
        timer = timer + 1
        # while not trigger:
        r = requests.get(trigger_endpoint+access_token)
        rjson = r.json()
        for trigger_check_endpoint in trigger_check_endpoints:
            rjson = rjson[trigger_check_endpoint]
        if not original_count_flag:
            original_count = len(rjson)
            original_count_flag = True
        if len(rjson) > original_count:
            trigger = True
            break
        time.sleep(1)
    if not trigger:
        return 'TIMEOUT'

    # The new thing should be the last in the list
    the_new_thing = rjson.pop()

    # Save the thing_to_remember in the database
    thing_to_remember = get_data_at_endpoint(the_new_thing, thing_to_remember_endpoints)
    thing_to_remember_db = Thing_to_remember(access_token,thing_to_remember)
    db.session.add(thing_to_remember_db)
    db.session.commit()

    # Return the value at the trigger_value endpoint
    new_thing_name = get_data_at_endpoint(the_new_thing, trigger_value_endpoints)
    return '{"newThingName":"'+new_thing_name+'"}'

@app.route('/get_remembered_thing', methods=['POST'])
def get_remembered_thing():
    access_token = request.args['access_token']
    trigger_endpoint = request.form['triggerEndpoint']
    trigger_check_endpoint = request.form['triggerCheck']
    trigger_value_endpoint = request.form['triggerValue']
    things_to_remember = Thing_to_remember.query.filter_by(access_token=access_token).all()
    thing_to_remember = things_to_remember.pop() # Get just the last thing
    trigger_endpoint = trigger_endpoint.replace('replace_me',str(thing_to_remember))
    counter = 0
    while counter < 60:
        r = requests.get(trigger_endpoint+access_token)
        rjson = r.json()
        if trigger_check_endpoint in rjson:
            # if trigger_value_endpoint in rjson:
            new_data = rjson[trigger_check_endpoint]
            return '{"newData":"'+new_data+'"}'
        counter = counter + 1
        time.sleep(1)
    return 'TIMEOUT'

@app.route('/get_added_data', methods=['POST'])
def get_added_data():
    # Doesn't actually need to return the photo from FB.
    access_token = request.args['access_token']
    trigger_endpoint = request.form['triggerEndpoint']
    trigger_check_endpoints = request.form['triggerCheck'].split(',')
    trigger_value = request.form['triggerValue']
    trigger_value2_endpoints = request.form['thingToRemember'].split(',')
    things_to_remember = Thing_to_remember.query.filter_by(access_token=access_token).all()
    thing_to_remember = things_to_remember.pop() # Get just the last thing
    trigger_endpoint = trigger_endpoint.replace('replace_me',str(thing_to_remember))
    counter = 0
    while counter < 60:
        r = requests.get(trigger_endpoint+access_token)
        rjson = r.json()
        # Check if certain endpoint equals something
        trigger_check = get_data_at_endpoint(rjson, trigger_check_endpoints)
        trigger_value2 = get_data_at_endpoint(rjson, trigger_value2_endpoints)
        trigger_value = autoconvert(trigger_value)
        if trigger_check == trigger_value:
            new_data = trigger_value2
            return '{"newData":"'+new_data+'"}'
        counter = counter + 1
        time.sleep(1)
    return 'TIMEOUT'

@app.route('/choose_next_step', methods=['POST'])
def choose_next_step():
    choice = request.args['choice']
    choice_one = request.form['triggerCheck']
    choice_two = request.form['triggerValue']
    if choice == 'choice_one':
        return '{"chosenStep":"'+choice_one+'"}'
    if choice == 'choice_two':
        return '{"chosenStep":"'+choice_two+'"}'

            
        








