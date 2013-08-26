from flask import Flask, request, redirect, render_template, url_for, make_response
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.restless
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.admin import Admin
from flask.ext.heroku import Heroku
import hashlib
from datetime import datetime
import os, requests, json, time
from requests import get as http_get
#----------------------------------------
# initialization
#----------------------------------------

app = Flask(__name__)
heroku = Heroku(app) # Sets CONFIG automagically

app.config.update(
    DEBUG = True,
    SQLALCHEMY_DATABASE_URI = 'postgres://hackyourcity@localhost/howtocity',
    # SQLALCHEMY_DATABASE_URI = 'postgres://postgres:root@localhost/howtocity',
    # SECRET_KEY = '123456'
)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)
api_version = '/api/v1'

def add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization'
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
    long_description = db.Column(db.Unicode)
    short_description = db.Column(db.Unicode)
    time_estimate = db.Column(db.Unicode)
    difficulty = db.Column(db.Unicode)
    additional_resources = db.Column(db.Unicode)
    tips = db.Column(db.Unicode)
    third_party_service = db.Column(db.Unicode)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('lessons', lazy='dynamic'))

    def __init__(self, name=None, description=None, long_description=None, short_description=None, time_estimate=None, difficulty=None, additional_resources=None, tips=None, third_party_service=None):
        self.name = name
        self.long_description = long_description
        self.short_description = short_description
        self.time_estimate = time_estimate
        self.difficulty = difficulty
        self.additional_resources = additional_resources
        self.tips = tips
        self.third_party_service = third_party_service

    def __repr__(self):
        return self.name

class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    step_type = db.Column(db.Unicode)
    step_number = db.Column(db.Integer)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    lesson = db.relationship('Lesson', backref=db.backref('steps', lazy='dynamic'))
    step_text = db.Column(db.Unicode)
    trigger_endpoint = db.Column(db.Unicode)
    trigger_check = db.Column(db.Unicode)
    trigger_value = db.Column(db.Unicode)
    thing_to_remember = db.Column(db.Unicode)
    feedback = db.Column(db.Unicode)
    next_step_number = db.Column(db.Integer)

    def __init__(self, name=None, step_number=None, step_type=None, step_text=None, trigger_endpoint=None, trigger_check=None, trigger_value=None, thing_to_remember=None, feedback=None, next_step_number=None):
        self.name = name
        self.step_number = step_number
        self.step_type = step_type
        self.step_text = step_text
        self.trigger_endpoint = trigger_endpoint
        self.trigger_check = trigger_check
        self.trigger_value = trigger_value
        self.thing_to_remember = thing_to_remember
        self.feedback = feedback
        self.next_step_number = next_step_number

    def __repr__(self):
        return self.name

class Bf_user(db.Model):
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Unicode, nullable=False, unique=True)
    password = db.Column(db.Unicode, nullable=False)
    access_token = db.Column(db.Unicode, nullable=False)
    name = db.Column(db.Unicode, nullable=False)
    # Relations
    lessons = db.relationship("UserLesson")

    # TODO: Decide how strict this email validation should be
    # @validates('email')
    # def validate_email(self, key, address):
    #     pass

    def __init__(self, email=None, password=None, name=None):
        self.email = str(email)
        password = str(password)
        self.access_token = hashlib.sha256(str(os.urandom(24))).hexdigest()
        self.password = self.pw_digest(password)
        self.name = name

    def __repr__(self):
        return "Bf_user email: %s, id: %s" %(self.email, self.id)

    def pw_digest(self, password):
        # Hash password, store it with random signature for rehash
        salt = hashlib.sha256(str(os.urandom(24))).hexdigest()
        hsh = hashlib.sha256(salt + password).hexdigest()
        return '%s$%s' % (salt, hsh)

    def check_pw(self, raw_password):
        salt, hsh = self.password.split('$')
        return hashlib.sha256(salt + raw_password).hexdigest() == hsh

    def make_authd_req(self, service, req_url):
        for connection in self.connections:
            if connection.service == service:
                return http_get(req_url + connection.access_token, headers={'User-Agent': 'Python'})

class UserLesson(db.Model):
    __tablename__ = 'user_to_lesson'
    user_id = db.Column(db.Integer, db.ForeignKey('bf_user.id'),
        primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'),
        primary_key=True)
    recent_step = db.Column(db.Integer, db.ForeignKey('step.id'))
    start_dt = db.Column(db.DateTime)
    end_dt = db.Column(db.DateTime, nullable=True)
    lesson = db.relationship('Lesson')

    def __init__(self, start_dt=None, end_dt=None, recent_step=None):
        self.start_dt = start_dt 
        self.end_dt = end_dt

    def __repr__(self):
        return "User_to_lesson user_id: %s, lesson_id: %s" % (self.user_id, self.lesson_id)

class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('bf_user.id'))
    user = db.relationship('Bf_user', backref=db.backref('connections', lazy='dynamic'))
    service = db.Column(db.Unicode)
    access_token = db.Column(db.Unicode)

    def __init__(self, service=None, access_token=None):
        self.service = service
        self.access_token = access_token

    def __repr__(self):
        return "Connection user_id: %s, service: %s" % (self.user_id, self.service)


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
manager.create_api(Category, methods=['GET', 'POST', 'DELETE'], url_prefix=api_version, collection_name='categories')
manager.create_api(Lesson, methods=['GET', 'POST', 'DELETE'], url_prefix=api_version, collection_name='lessons')
manager.create_api(Step, methods=['GET', 'POST', 'DELETE'], url_prefix=api_version, collection_name='steps')
# manager.create_api(Bf_user, methods=['GET', 'POST', 'DELETE'], url_prefix=api_version, collection_name='users')
# manager.create_api(UserLesson, methods=['GET', 'POST', 'DELETE'], url_prefix=api_version, collection_name='userlessons')

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

# class Bf_userView(ModelView):
#     column_display_pk = True
#     column_auto_select_related = True

# class UserLessonView(ModelView):
#     column_display_pk = True
#     column_auto_select_related = True

admin.add_view(CategoryView(Category, db.session))
admin.add_view(LessonView(Lesson, db.session))
admin.add_view(StepView(Step, db.session))
# admin.add_view(Bf_userView(Bf_user, db.session))
# admin.add_view(UserLessonView(UserLesson, db.session))

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
    # Check if the user is has a third_party_service access token.
    response = {
        "logged_in" : False,
        "timeout" : True
    }
    # Require Authorization header for this endpoint
    if 'Authorization' in request.headers:
        htc_access = request.headers['Authorization']
    else:
        response['error'] = 'Authorization required'
        return make_response(response, 403)
    # Check database for connection between this user and this service
    service_name = request.form['lessonService'].lower()
    cur_user = Bf_user.query.filter_by(access_token=htc_access).first()
    if not cur_user:
        response['status'] = 404
        response['error'] = 'No user found.'
    else:
        for connection in cur_user.connections:
            if connection.service == service_name:
                response['status'] = 200
                response['logged_in'] = True
                response['timeout'] = False
    # Build proper Response to return
    response = make_response(json.dumps(response), response['status'])
    response.headers['content-type'] = 'application/json'
    return response

@app.route('/check_for_new', methods=['POST'])
def check_for_new():
    # Check if something new gets added to the 
    # triggerCheck of the triggerEndpoint.
    # When something new appears, remember the thingToRemember
    # then return the triggerValue.
    response = {
        "new_thing_name" : False,
        "timeout" : True
    }
    # Require Authorization header for this endpoint
    if 'Authorization' in request.headers:
        htc_access = request.headers['Authorization']
    else:
        response['error'] = 'Authorization required'
        return make_response(response, 403)
    service_name = request.form['lessonService'].lower()
    cur_user = Bf_user.query.filter_by(access_token=htc_access).first()
    trigger_endpoint = request.form['triggerEndpoint']
    trigger_check_endpoints = request.form['triggerCheck'].split(',')
    trigger_value_endpoints = request.form['triggerValue'].split(',')
    thing_to_remember_endpoints = request.form['thingToRemember'].split(',')
    trigger = False
    original_count = 10000000
    original_count_flag = False
    timer = 0
    while timer < 5:
        timer = timer + 1
        r = cur_user.make_authd_req(service_name, trigger_endpoint)
        rjson = r.json()
        print rjson
        for trigger_check_endpoint in trigger_check_endpoints:
            trigger_check_endpoint = autoconvert(trigger_check_endpoint)
            rjson = rjson[trigger_check_endpoint]
        if not original_count_flag:
            original_count = len(rjson)
            original_count_flag = True
        if len(rjson) > original_count:
            trigger = True
            break
        time.sleep(1)
    if not trigger:
        return make_response(json.dumps(response), 200)

    # Default
    # if third_party_service == 'facebook':
    # Facebook has new pages appear at the end of the list
    the_new_thing = rjson.pop()

    # if third_party_service == 'foursquare':
    #     # Foursquare has new tips as the first in the list
    #     the_new_thing = rjson.pop(0)

    # Save the thing_to_remember in the database
    # Todo: Better temporary way to remember something.
    # Only remember one thing per user.
    thing_to_remember = get_data_at_endpoint(the_new_thing, thing_to_remember_endpoints)
    thing_to_remember_db = Thing_to_remember.query.filter_by(access_token=htc_access).first()
    if thing_to_remember_db:
        thing_to_remember_db.thing_to_remember = thing_to_remember
    else:
        thing_to_remember_db = Thing_to_remember(htc_access,thing_to_remember)
        db.session.add(thing_to_remember_db)
    db.session.commit()

    # Return the value at the trigger_value endpoint
    response["new_thing_name"] = get_data_at_endpoint(the_new_thing, trigger_value_endpoints)
    response['timeout'] = False
    response = make_response(json.dumps(response), 200)
    response.headers['content-type'] = 'application/json'
    return response


# Refactor to combine with the above
@app.route('/check_for_new_tip', methods=['POST'])
def check_for_new_tip():

    response = {
        "new_tip_added" : False,
        "timeout" : True
    }
    # Require Authorization header for this endpoint
    if 'Authorization' in request.headers:
        htc_access = request.headers['Authorization']
    else:
        response['error'] = 'Authorization required'
        return make_response(json.dumps(response), 403)
    third_party_service = request.form['thirdPartyService']
    trigger_endpoint = request.form['triggerEndpoint']
    trigger_check_endpoints = request.form['triggerCheck'].split(',')
    trigger_value_endpoints = request.form['triggerValue'].split(',')
    thing_to_remember_endpoints = request.form['thingToRemember'].split(',')
    trigger = False
    original_count = 10000000
    original_count_flag = False
    timer = 0
    while timer < 5:
        timer = timer + 1
        r = requests.get(trigger_endpoint+htc_access)
        rjson = r.json()
        for trigger_check_endpoint in trigger_check_endpoints:
            trigger_check_endpoint = autoconvert(trigger_check_endpoint)
            rjson = rjson[trigger_check_endpoint]
        if not original_count_flag:
            original_count = len(rjson)
            original_count_flag = True
        if len(rjson) > original_count:
            response['new_tip_added'] = True
        time.sleep(1)
    response = make_response(json.dump(response), 200)
    response.headers['content-type'] = 'application/json'
    return response

@app.route('/get_remembered_thing', methods=['POST'])
def get_remembered_thing():
    # Grabs the remembered thing.
    # Bug: If the user signs in from a different browser, we won't be able to remember thing.
    response = {
        "new_data" : False,
        "timeout" : True
    }
    # Require Authorization header for this endpoint
    if 'Authorization' in request.headers:
        htc_access = request.headers['Authorization']
    else:
        response['error'] = 'Authorization required'
        return make_response(json.dumps(response), 403)
    cur_user = Bf_user.query.filter_by(access_token=htc_access).first()
    service_name = request.form['lessonService'].lower()
    trigger_endpoint = request.form['triggerEndpoint']
    trigger_check_endpoint = request.form['triggerCheck']
    trigger_value_endpoint = request.form['triggerValue']
    things_to_remember = Thing_to_remember.query.filter_by(access_token=htc_access).all()
    thing_to_remember = things_to_remember.pop() # Get just the last thing
    trigger_endpoint = trigger_endpoint.replace('replace_me',str(thing_to_remember))

    timer = 0
    while timer < 5:
        r = cur_user.make_authd_req(service_name, trigger_endpoint)
        rjson = r.json()
        if trigger_check_endpoint in rjson:
            # if trigger_value_endpoint in rjson:
            response["new_data"] = rjson[trigger_check_endpoint]
            response['timeout'] = False
            response = make_response(json.dumps(response), 200)
            response.headers['content-type'] = 'application/json'
            return response
        timer = timer + 1
        time.sleep(1)
    response = make_response(response, 200)
    response.headers['content-type'] = 'application/json'
    return response

@app.route('/get_added_data', methods=['POST'])
def get_added_data():
    # Checks to see if new data was added to triggerEndpoint.
    # Once triggerCheck equals triggerValue
    # then return thingToRemember column (need to make a new column with better name) 
    response = {
        "new_data" : False,
        "timeout" : True
    }
    # Require Authorization header for this endpoint
    if 'Authorization' in request.headers:
        htc_access = request.headers['Authorization']
    else:
        response['error'] = 'Authorization required'
        return make_response(json.dumps(response), 403)
    cur_user = Bf_user.query.filter_by(access_token=htc_access).first()
    service_name = request.form['lessonService'].lower()
    trigger_endpoint = request.form['triggerEndpoint']
    trigger_check_endpoints = request.form['triggerCheck'].split(',')
    trigger_value = request.form['triggerValue']
    trigger_value2_endpoints = request.form['thingToRemember'].split(',')
    thing_to_remember = Thing_to_remember.query.filter_by(access_token=htc_access).first()
    trigger_endpoint = trigger_endpoint.replace('replace_me',str(thing_to_remember))
    timer = 0
    while timer < 5:
        r = cur_user.make_authd_req(service_name, trigger_endpoint)
        rjson = r.json()
        trigger_check = get_data_at_endpoint(rjson, trigger_check_endpoints)
        trigger_value2 = get_data_at_endpoint(rjson, trigger_value2_endpoints)
        trigger_value = autoconvert(trigger_value)
        if trigger_check == trigger_value:
            response["new_data"] = trigger_value2
            response['timeout'] = False
            response = make_response(json.dumps(response), 200)
            response.headers['content-type'] = 'application/json'
            return response
        timer = timer + 1
        time.sleep(1)
    response = make_response(response, 200)
    response.headers['content-type'] = 'application/json'
    return response

@app.route('/signup', methods=['POST'])
def htc_signup():
    user_email = request.form['email']
    user_pw = request.form['password']
    user_name = request.form['name']
    cur_user = Bf_user(user_email, user_pw, user_name)
    response = {}

    if (Bf_user.query.filter_by(email=user_email).first()):
        response['error'] = 'Email already in use.'
        response['status'] = 400
        response = make_response(json.dumps(response), 403)
        response.headers['content-type'] = 'application/json'
        return response
    else:        
        db.session.add(cur_user)
        db.session.commit()

    response['access_token'] = cur_user.access_token 
    response['token_type'] = 'bearer'
    response['email'] = cur_user.email
    response['name'] = cur_user.name
    response['status'] = 200
    # Return a proper response with correct headers
    response = make_response(json.dumps(response), 200)
    response.headers['content-type'] = 'application/json'
    return response

@app.route('/signin', methods=['POST'])
def htc_signin():
    user_email = request.form['email']
    user_password = request.form['password']
    cur_user = Bf_user.query.filter_by(email=user_email).first()
    response = {}
    if cur_user and cur_user.check_pw(user_password):
        # User is valid, return credentials
        response['access_token'] = cur_user.access_token
        response['token_type'] = "bearer"
        response['email'] = cur_user.email
        response['name'] = cur_user.name
        response['status'] = 200
    else:
        response['status'] = 403
        response['error'] = "Invalid login credentials."
    response = make_response(json.dumps(response), 200)
    response.headers['content-type'] = 'application/json'
    return response

@app.route('/create_connection', methods=['POST'])
def create_connection():    
    response = {
        "connection_saved" : False
    }

    service_name = request.form['service']
    oauth_token = request.form['service_access']
    # Require Authorization header for this endpoint
    if 'Authorization' in request.headers:
        htc_access = request.headers['Authorization']
    else:
        response['error'] = 'Authorization required'
        return make_response(response, 403)
    cur_user = Bf_user.query.filter_by(access_token=htc_access).first()
    if not cur_user:
        response['error'] = 'User not found'
        return make_response(json.dumps(response), 404)
    # Update exisitng connection with new oauth token
    connectionUpdatedFlag = False
    for connection in cur_user.connections:
        if connection.service == service_name:
            connectionUpdatedFlag = True
            connection.access_token = oauth_token
    # Make a new connection if there isnt one
    if not connectionUpdatedFlag:
        new_connection = Connection(service_name, oauth_token)
        cur_user.connections.append(new_connection)
    db.session.commit()
    response['connection_saved'] = True
    response = make_response(json.dumps(response), 200)
    response.headers['content-type'] = 'application/json'
    return response

@app.route('/record_step', methods=['POST'])
def record_step():
    # import pdb; pdb.set_trace()
    response = {}
    lesson_id = request.form['lessonId']
    step_id = request.form['id']
    # Require Authorization header for this endpoint
    if 'Authorization' in request.headers:
        htc_access = request.headers['Authorization']
    else:
        response['error'] = 'Authorization required'
        return make_response(json.dumps(response), 403)
    cur_user = Bf_user.query.filter_by(access_token=htc_access).first()
    cur_less = Lesson.query.filter_by(id=lesson_id).first()
    user_less = UserLesson(start_dt=datetime.now())
    # Already started the lesson, just alter recent step
    for lesson in cur_user.lessons:
        if lesson.lesson_id == cur_less.id:
            if step_id > lesson.recent_step:
                lesson.recent_step = step_id
            # If final step in lesson, update end_dt
            step_count = max([step.step_number for step in cur_less.steps])
            if Step.query.get(step_id).step_number == step_count:
                lesson.end_dt = datetime.now()
            db.session.commit()
            response = make_response(json.dumps(response), 200)
            response.headers['content-type'] = 'application/json'
            return response
    # New to the lesson, append it to user lesson association
    if cur_user and cur_less:
        cur_less.recent_step = step_id
        user_less.lesson = cur_less
        cur_user.lessons.append(user_less)
        db.session.commit()
        response['status'] = 200
    else:
        response['status'] = 404
        response['error'] = "Unable to save lesson state."

    response = make_response(json.dumps(response), response['status'])
    response.headers['content-type'] = 'application/json'
    return response

