from flask import Flask, request, redirect, render_template
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
    SQLALCHEMY_DATABASE_URI = 'postgres://hackyourcity@localhost/howtocity',
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
    column_list = ('lesson_id','lesson','id','name','step_number','step_type','step_text','trigger_endpoint','trigger_check','trigger_value','thing_to_remember','feedback','next_step_number')
    column_sortable_list = (('lesson_id',Lesson.id),'name','step_type')

admin.add_view(CategoryView(Category, db.session))
admin.add_view(LessonView(Lesson, db.session))
admin.add_view(StepView(Step, db.session))

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

    access_token = request.args['access_token']
    third_party_service = request.form['thirdPartyService']
    resource_url = request.form['currentStep[triggerEndpoint]']
    path_for_objects = request.form['currentStep[triggerCheck]'].split(',')
    path_for_attribute_to_display = request.form['currentStep[triggerValue]'].split(',')
    path_for_attribute_to_remember = request.form['currentStep[thingToRemember]'].split(',')
    original_count = autoconvert(request.form['originalCount'])
    # If original_count is false in post data, then just return the count of objects at the endpoint.
    if not original_count:
        resource = requests.get(resource_url+access_token)
        resource = resource.json()
        for key in path_for_objects:
            key = autoconvert(key)
            resource = resource[key]
        original_count = len(resource)
        our_response["original_count"] = original_count
        our_response["timeout"] = False
        return json.dumps(our_response)

    #  Check api_resource_url every two seconds for a new addition at path_of_resource_to_check
    timer = 0
    while timer < 60:
        resource = requests.get(resource_url+access_token)
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
        return json.dumps(our_response) # timeout
    else:
        our_response["timeout"] = False

    # Facebook has new pages appear at the end of the list
    if third_party_service == 'facebook':
        the_new_object = resource.pop()
    # Foursquare has new tips as the first in the list
    if third_party_service == 'foursquare':
        the_new_object = resource.pop(0)

    # Return an attribute to display
    our_response["attribute_to_display"] = get_data_at_endpoint(the_new_object, path_for_attribute_to_display)
    # Remember an attribute of the new object
    our_response["attribute_to_remember"] = get_data_at_endpoint(the_new_object, path_for_attribute_to_remember)
    return json.dumps(our_response)

@app.route('/check_if_attribute_exists', methods=['POST'])
def check_if_attribute_exists():
    # Check if attribute exists
    # Return attribute

    our_response = {
        "attribute_exists" : False,
        "attribute_to_display" : False,
        "timeout" : True
    }

    access_token = request.args['access_token']
    resource_url = request.form['currentStep[triggerEndpoint]']
    remembered_attribute = request.form['rememberedAttribute']
    try:
        resource_url = resource_url.replace('replace_me',remembered_attribute)
    except:
        pass
    path_for_attribute_to_display = request.form['currentStep[triggerCheck]'].split(',')
    
    # Check api_resource_url every two seconds for a value
    timer = 0
    while timer < 60:
        resource = requests.get(resource_url+access_token)
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

    access_token = request.args['access_token']
    resource_url = request.form['currentStep[triggerEndpoint]']
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
        resource = requests.get(resource_url+access_token)
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

    access_token = request.args['access_token']
    resource_url = request.form['currentStep[triggerEndpoint]']
    remembered_attribute = request.form['rememberedAttribute']
    try:
        resource_url = resource_url.replace('replace_me',remembered_attribute)
    except:
        pass
    path_for_attribute = request.form['currentStep[triggerCheck]'].split(',')
    path_for_attribute_2 = request.form['currentStep[triggerValue]'].split(',')
    path_for_attribute_3 = request.form['currentStep[thingToRemember]'].split(',')

    resource = requests.get(resource_url+access_token)
    resource = resource.json()
    our_response["attribute"] = get_data_at_endpoint(resource, path_for_attribute)
    our_response["attribute_2"] = get_data_at_endpoint(resource, path_for_attribute_2)
    our_response["attribute_3"] = get_data_at_endpoint(resource, path_for_attribute_3)
    return json.dumps(our_response)



# # Refactor to combine with check_for_new
# @app.route('/check_for_new_tip', methods=['POST'])
# def check_for_new_tip():

#     response = {
#         "new_tip_added" : False,
#         "timeout" : True
#     }

#     access_token = request.args['access_token']
#     third_party_service = request.form['thirdPartyService']
#     trigger_endpoint = request.form['triggerEndpoint']
#     trigger_check_endpoints = request.form['triggerCheck'].split(',')
#     trigger_value_endpoints = request.form['triggerValue'].split(',')
#     thing_to_remember_endpoints = request.form['thingToRemember'].split(',')
#     trigger = False
#     original_count = 10000000
#     original_count_flag = False
#     timer = 0
#     while timer < 60:
#         timer = timer + 1
#         r = requests.get(trigger_endpoint+access_token)
#         rjson = r.json()
#         for trigger_check_endpoint in trigger_check_endpoints:
#             trigger_check_endpoint = autoconvert(trigger_check_endpoint)
#             rjson = rjson[trigger_check_endpoint]
#         if not original_count_flag:
#             original_count = len(rjson)
#             original_count_flag = True
#         if len(rjson) > original_count:
#             response['new_tip_added'] = True
#         time.sleep(1)
#     return json.dumps(response)

# @app.route('/get_remembered_thing', methods=['POST'])
# def get_remembered_thing():

#     response = {
#         "new_data" : False,
#         "timeout" : True
#     }

#     access_token = request.args['access_token']
#     trigger_endpoint = request.form['triggerEndpoint']
#     trigger_check_endpoint = request.form['triggerCheck']
#     trigger_value_endpoint = request.form['triggerValue']
#     things_to_remember = Thing_to_remember.query.filter_by(access_token=access_token).all()
#     thing_to_remember = things_to_remember.pop() # Get just the last thing
#     trigger_endpoint = trigger_endpoint.replace('replace_me',str(thing_to_remember))
#     timer = 0
#     while timer < 60:
#         r = requests.get(trigger_endpoint+access_token)
#         rjson = r.json()
#         if trigger_check_endpoint in rjson:
#             # if trigger_value_endpoint in rjson:
#             response["new_data"] = rjson[trigger_check_endpoint]
#             response['timeout'] = False
#             return json.dumps(response)
#         timer = timer + 1
#         time.sleep(1)
#     return json.dumps(response)
