from flask import Flask, request, redirect, render_template, url_for, make_response
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.restless
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.admin import Admin
from flask.ext.heroku import Heroku
import hashlib
from datetime import datetime
import os, requests, json, time, re
#----------------------------------------
# initialization
#----------------------------------------

app = Flask(__name__)
heroku = Heroku(app) # Sets CONFIG automagically

app.config.update(
    DEBUG = True,
    SQLALCHEMY_DATABASE_URI = 'postgres://hackyourcity@localhost/howtocity',
    # SQLALCHEMY_DATABASE_URI = 'postgres://postgres:root@localhost/howtocity',
    SECRET_KEY = '123456'
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

    def make_authorized_request(self, service, req_url):
        for connection in self.connections:
            if connection.service == service:
                return requests.get(req_url + connection.access_token, headers={'User-Agent': 'Python'})

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
    user = db.relationship('Bf_user')

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

# API ------------------------------------------------------------
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Category, methods=['GET', 'POST', 'DELETE'], url_prefix=api_version, collection_name='categories')
manager.create_api(Lesson, methods=['GET', 'POST', 'DELETE'], url_prefix=api_version, collection_name='lessons')
manager.create_api(Step, methods=['GET', 'POST', 'DELETE'], url_prefix=api_version, collection_name='steps')
# manager.create_api(Bf_user, methods=['GET', 'POST', 'DELETE'], url_prefix=api_version, collection_name='users')
includes = ['lesson','lesson.name','lesson.id','user','user.name','end_dt']
manager.create_api(UserLesson, include_columns=includes, methods=['GET', 'POST', 'DELETE'], url_prefix=api_version, collection_name='userlessons')

# ADMIN ------------------------------------------------------------
admin = Admin(app, name='BizFriend.ly Admin', url='/api/admin')

class CategoryView(ModelView):
    column_display_pk = True

class LessonView(ModelView):
    column_display_pk = True
    column_auto_select_related = True

class StepView(ModelView):
    column_display_pk = True
    column_auto_select_related = True
    column_list = ('lesson_id','lesson','id','name','step_number','step_type','step_text','trigger_endpoint','trigger_check','trigger_value','thing_to_remember','feedback','next_step_number')
    column_sortable_list = (('lesson_id',Lesson.id),'name','step_type')

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
        endpoint = autoconvert(endpoint)
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


@app.route('/check_for_new', methods=['POST'])
def check_for_new():
    # Check once for original count of objects
    # then check if new object exists
    # Remember new object
    # Return desired endpoint

    our_response = {
        "attribute_to_display" : False,
        "attribute_to_remember" : False,
        "new_object_added" : False,
        "original_count" : False,
        "timeout" : True
    }

    # Require Authorization header for this endpoint
    if 'Authorization' in request.headers:
        htc_access = request.headers['Authorization']
    else:
        response['error'] = 'Authorization required'
        return make_response(response, 403)

    current_user = Bf_user.query.filter_by(access_token=htc_access).first()
    
    third_party_service = request.form['thirdPartyService']
    
    # if app.config['DEBUG']:
    #     if third_party_service == 'facebook':
    #         our_response = {
    #             "attribute_to_display" : "TEST PAGE",
    #             "attribute_to_remember" : 297429370396923,
    #             "new_object_added" : True,
    #             "original_count" : 10000000,
    #             "timeout" : False
    #         }

    resource_url = request.form['currentStep[triggerEndpoint]']
    if 'rememberedAttribute' in request.form:
        remembered_attribute = request.form['rememberedAttribute']
    try:
        resource_url = resource_url.replace('replace_me',remembered_attribute)
    except:
        pass
    path_for_objects = request.form['currentStep[triggerCheck]'].split(',')
    path_for_attribute_to_display = request.form['currentStep[triggerValue]'].split(',')
    path_for_attribute_to_remember = request.form['currentStep[thingToRemember]'].split(',')
    original_count = autoconvert(request.form['originalCount'])
    # If original_count is false in post data, then just return the count of objects at the endpoint.
    if not original_count:
        # r = current_user.make_authorized_request(service_name, trigger_endpoint)
        resource = current_user.make_authorized_request(third_party_service, resource_url)
        resource = resource.json()
        for key in path_for_objects:
            key = autoconvert(key)
            try:
                resource = resource[key]
            except IndexError:
                # Foursquare, its an empty list when its new.
                break
        original_count = len(resource)
        our_response["original_count"] = original_count
        our_response["timeout"] = False
        return make_response(json.dumps(our_response), 200)

    #  Check api_resource_url every two seconds for a new addition at path_of_resource_to_check
    timer = 0
    while timer < 60:
        resource = current_user.make_authorized_request(third_party_service, resource_url)
        resource = resource.json()
        for key in path_for_objects:
            key = autoconvert(key)
            resource = resource[key] 
        if len(resource) > original_count:
            our_response["new_object_added"] = True
            break
        time.sleep(2)
        timer = timer + 2
    if not our_response["new_object_added"]:
        return make_response(json.dumps(our_response), 200) # timeout
    else:
        our_response["timeout"] = False
    if third_party_service == 'facebook':
        the_new_object = resource.pop()
    # Foursquare has new tips as the first in the list
    if third_party_service == 'foursquare':
        the_new_object = resource.pop(0)

    # Return an attribute to display if its not blank.
    if path_for_attribute_to_display[0]:
        our_response["attribute_to_display"] = get_data_at_endpoint(the_new_object, path_for_attribute_to_display)
    # Remember an attribute of the new object if its not blank.
    if path_for_attribute_to_remember[0]:
        our_response["attribute_to_remember"] = get_data_at_endpoint(the_new_object, path_for_attribute_to_remember)
    return make_response(json.dumps(our_response), 200)


@app.route('/check_if_attribute_exists', methods=['POST'])
def check_if_attribute_exists():
    # Check if attribute exists
    # Return attribute

    our_response = {
        "attribute_exists" : False,
        "attribute_to_display" : False,
        "timeout" : True
    }

    # Require Authorization header for this endpoint
    if 'Authorization' in request.headers:
        htc_access = request.headers['Authorization']
    else:
        response['error'] = 'Authorization required'
        return make_response(response, 403)

    current_user = Bf_user.query.filter_by(access_token=htc_access).first()

    third_party_service = request.form['thirdPartyService']
    resource_url = request.form['currentStep[triggerEndpoint]']
    if 'rememberedAttribute' in request.form:
        remembered_attribute = request.form['rememberedAttribute']
    try:
        resource_url = resource_url.replace('replace_me',remembered_attribute)
    except:
        pass
    path_for_attribute_to_display = request.form['currentStep[triggerCheck]'].split(',')
    
    # Check api_resource_url every two seconds for a value
    timer = 0
    while timer < 60:
        resource = current_user.make_authorized_request(third_party_service, resource_url)
        resource = resource.json()
        for key in path_for_attribute_to_display:
            key = autoconvert(key)
            if key in resource:
                resource = resource[key]
        # If resource is still a dict, we didn't find what we were looking for.
        if type(resource) != dict:
            our_response["attribute_exists"] = True
            our_response["attribute_to_display"] = resource
            our_response["timeout"] = False
            return json.dumps(our_response)
        time.sleep(2)
        timer = timer + 2
    return json.dumps(our_response)


@app.route('/check_attribute_for_value', methods=['POST'])
def check_attribute_for_value():
    # Check attribute for value
    # If it matches, return other attribute
    our_response = {
        "attribute_value_matches" : False,
        "attribute_to_display" : False,
        "timeout" : True
    }

    # Require Authorization header for this endpoint
    if 'Authorization' in request.headers:
        htc_access = request.headers['Authorization']
    else:
        response['error'] = 'Authorization required'
        return make_response(response, 403)

    current_user = Bf_user.query.filter_by(access_token=htc_access).first()

    third_party_service = request.form['thirdPartyService']
    resource_url = request.form['currentStep[triggerEndpoint]']
    if 'rememberedAttribute' in request.form:
        remembered_attribute = request.form['rememberedAttribute']
    try:
        resource_url = resource_url.replace('replace_me',remembered_attribute)
    except:
        pass
    trigger_checks = request.form['currentStep[triggerCheck]'].split(',')
    trigger_value = request.form['currentStep[triggerValue]']
    path_for_attribute_to_display = request.form['currentStep[thingToRemember]'].split(',')

    timer = 0
    while timer < 60:
        resource = current_user.make_authorized_request(third_party_service, resource_url)
        resource = resource.json()
        trigger_check = get_data_at_endpoint(resource, trigger_checks)
        trigger_value = autoconvert(trigger_value)
        if trigger_check == trigger_value:
            our_response["attribute_value_matches"] = True
            our_response["attribute_to_display"] = get_data_at_endpoint(resource,path_for_attribute_to_display)
            our_response["timeout"] = False
            return json.dumps(our_response)
        time.sleep(2)
        timer = timer + 2
    return json.dumps(our_response)


@app.route('/get_attributes', methods=['POST'])
def get_attributes():
    # Get the attributes from the resource_url
    # If remembered_attributes exists, use that as the id
    our_response = {
        "attribute" : False,
        "attribute_2" : False,
        "attribute_3" : False
    }

    # Require Authorization header for this endpoint
    if 'Authorization' in request.headers:
        htc_access = request.headers['Authorization']
    else:
        response['error'] = 'Authorization required'
        return make_response(response, 403)

    current_user = Bf_user.query.filter_by(access_token=htc_access).first()

    third_party_service = request.form['thirdPartyService']
    resource_url = request.form['currentStep[triggerEndpoint]']
    if 'rememberedAttribute' in request.form:
        remembered_attribute = request.form['rememberedAttribute']
    try:
        resource_url = resource_url.replace('replace_me',remembered_attribute)
    except:
        pass
    path_for_attribute = request.form['currentStep[triggerCheck]'].split(',')
    path_for_attribute_2 = request.form['currentStep[triggerValue]'].split(',')
    path_for_attribute_3 = request.form['currentStep[thingToRemember]'].split(',')

    resource = current_user.make_authorized_request(third_party_service, resource_url)
    resource = resource.json()
    try:
        our_response["attribute"] = get_data_at_endpoint(resource, path_for_attribute)
    except KeyError:
        pass
    try:
        our_response["attribute_2"] = get_data_at_endpoint(resource, path_for_attribute_2)
    except KeyError:
        pass
    try:
        our_response["attribute_3"] = get_data_at_endpoint(resource, path_for_attribute_3)
    except KeyError:
        pass
    return json.dumps(our_response)


@app.route('/signup', methods=['POST'])
def htc_signup():
    user_email = request.form['email']
    user_pw = request.form['password']
    user_name = request.form['name']
    response = {}

    # Validate emails
    if not re.match("^[a-zA-Z0-9_.+-]+\@[a-zA-Z0-9-]+\.+[a-zA-Z0-9]{2,4}$", user_email):
        response['error'] = 'That email doesn\'t look right.'
        response = make_response(json.dumps(response), 401)
        response.headers['content-type'] = 'application/json'
        return response

    current_user = Bf_user(user_email, user_pw, user_name)
    if (Bf_user.query.filter_by(email=user_email).first()):
        response['error'] = 'Someone has already signed up with that email.'
        response = make_response(json.dumps(response), 401)
        response.headers['content-type'] = 'application/json'
        return response
    else:        
        db.session.add(current_user)
        db.session.commit()

    response['access_token'] = current_user.access_token 
    response['token_type'] = 'bearer'
    response['email'] = current_user.email
    response['name'] = current_user.name
    # Return a proper response with correct headers
    response = make_response(json.dumps(response), 200)
    response.headers['content-type'] = 'application/json'
    return response


@app.route('/signin', methods=['POST'])
def htc_signin():
    user_email = request.form['email']
    user_password = request.form['password']
    response = {}

    # Validate emails
    if not re.match("^[a-zA-Z0-9_.+-]+\@[a-zA-Z0-9-]+\.+[a-zA-Z0-9]{2,4}$", user_email):
        response['error'] = 'That email doesn\'t look right.'
        response = make_response(json.dumps(response), 401)
        response.headers['content-type'] = 'application/json'
        return response

    current_user = Bf_user.query.filter_by(email=user_email).first()
    if current_user and current_user.check_pw(user_password):
        # User is valid, return credentials
        response['access_token'] = current_user.access_token
        response['token_type'] = "bearer"
        response['email'] = current_user.email
        response['name'] = current_user.name
        response['status'] = 200
        response = make_response(json.dumps(response),200)
    else:
        response['error'] = "Couldn't find your email and password."
        response = make_response(json.dumps(response),401)
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
        return make_response(response, 401)
    current_user = Bf_user.query.filter_by(access_token=htc_access).first()
    if not current_user:
        response['error'] = 'User not found'
        return make_response(json.dumps(response), 404)
    # Update exisitng connection with new oauth token
    connectionUpdatedFlag = False
    for connection in current_user.connections:
        if connection.service == service_name:
            connectionUpdatedFlag = True
            connection.access_token = oauth_token
    # Make a new connection if there isnt one
    if not connectionUpdatedFlag:
        new_connection = Connection(service_name, oauth_token)
        current_user.connections.append(new_connection)
    db.session.commit()
    response['connection_saved'] = True
    response = make_response(json.dumps(response), 200)
    response.headers['content-type'] = 'application/json'
    return response

@app.route('/record_step', methods=['POST'])
def record_step():
    response = {}
    lesson_id = request.form['lessonId']
    step_id = request.form['currentStep[id]']
    # Require Authorization header for this endpoint
    if 'Authorization' in request.headers:
        htc_access = request.headers['Authorization']
    else:
        response['error'] = 'Authorization required'
        return make_response(json.dumps(response), 401)
    current_user = Bf_user.query.filter_by(access_token=htc_access).first()
    cur_less = Lesson.query.filter_by(id=lesson_id).first()
    user_less = UserLesson(start_dt=datetime.now())
    # Already started the lesson, just alter recent step
    for lesson in current_user.lessons:
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
    if current_user and cur_less:
        cur_less.recent_step = step_id
        user_less.lesson = cur_less
        current_user.lessons.append(user_less)
        db.session.commit()
        response['status'] = 200
    else:
        response['status'] = 404
        response['error'] = "Unable to save lesson state."

    response = make_response(json.dumps(response), response['status'])
    response.headers['content-type'] = 'application/json'
    return response