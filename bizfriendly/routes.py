from flask import request, make_response
from bizfriendly import app
from models import *
from api import *

from datetime import datetime
import os, requests, json, time, re, boto, random
from boto.s3.key import Key
# from PIL import Image



# Helper Functions --------------------------------------------------------

# Traverses a path into a json object
def get_data_on_attribute_path(json_data, attributes):
    for attribute in attributes:
        attribute = autoconvert(attribute)
        json_data = json_data[attribute]
    data = json_data # Should be a string or int now, not json
    return data

# Convert to a python boolean
def boolify(s):
    if s == 'True' or s == 'true':
        return True
    if s == 'False' or s == 'false':
        return False
    raise ValueError("huh?")

# Convert string to a boolean, int, float, or list
def autoconvert(s):
    for fn in (boolify, int, float):
        try:
            return fn(s)
        except ValueError:
            pass
        if type(s) == unicode:
            if ',' in s:
                try:
                    return s.split(',')
                except AttributeError:
                    pass
    return s

# Routes --------------------------------------------------------

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
    
    if app.config['DEBUG']:
        if third_party_service == 'facebook':
            our_response = {
                "attribute_to_display" : "TEST PAGE",
                "attribute_to_remember" : 297429370396923,
                "new_object_added" : True,
                "original_count" : 10000000,
                "timeout" : False
            }
        if third_party_service == 'trello':
            step_number = autoconvert(request.form['currentStep[stepNumber]'])
            if step_number == 3:
                our_response = {
                    "attribute_to_display" : "BizFriendly Test Board",
                    "attribute_to_remember" : "52279d81c2fc68175a000609",
                    "new_object_added" : True,
                    "original_count" : 10000000,
                    "timeout" : False
                }

    resource_url = request.form['currentStep[triggerEndpoint]']
    if 'rememberedAttribute' in request.form:
        remembered_attribute = request.form['rememberedAttribute']
    try:
        resource_url = resource_url.replace('replace_me',remembered_attribute)
    except:
        pass
    # Check if a triggerCheck has been set.
    path_for_objects = False
    if request.form['currentStep[triggerCheck]']:
        path_for_objects = request.form['currentStep[triggerCheck]'].split(',')
    path_for_attribute_to_display = request.form['currentStep[triggerValue]'].split(',')
    path_for_attribute_to_remember = request.form['currentStep[thingToRemember]'].split(',')
    original_count = autoconvert(request.form['originalCount'])
    # If original_count is false in post data, then just return the count of objects at the endpoint.
    # original_count can be 0 so check not int instead of False
    if type(original_count) != int:
        # r = current_user.make_authorized_request(service_name, trigger_endpoint)
        resource = current_user.make_authorized_request(third_party_service, resource_url)
        resource = resource.json()
        if path_for_objects:
            for key in path_for_objects:
                key = autoconvert(key)
                if resource:
                    resource = resource[key]
        original_count = len(resource)
        our_response["original_count"] = original_count
        our_response["timeout"] = False
        return make_response(json.dumps(our_response), 200)

    #  Check api_resource_url every two seconds for a new addition at path_of_resource_to_check
    timer = 0
    while timer < 60:
        time.sleep(2)
        timer = timer + 2
        resource = current_user.make_authorized_request(third_party_service, resource_url)
        resource = resource.json()
        if path_for_objects:
            for key in path_for_objects:
                key = autoconvert(key)
                if resource:
                    resource = resource[key] 
        if len(resource) > original_count:
            our_response["new_object_added"] = True
            break
    if not our_response["new_object_added"]:
        return make_response(json.dumps(our_response), 200) # timeout
    else:
        our_response["timeout"] = False
    # Facebook pages are added to the end of the list.
    if third_party_service == 'facebook':
        the_new_resource = resource.pop()
    # Foursquare has new tips as the first in the list.
    if third_party_service == 'foursquare':
        the_new_resource = resource.pop(0)
    # Trello calls check_for_new twice
    if third_party_service == 'trello':
        step_number = autoconvert(request.form['currentStep[stepNumber]'])
        if step_number == 3:
            # Need to check timestamps of trello boards to find new.
            # Sort so newest is first in the list.
            resource.sort(key=lambda board : board["dateLastView"], reverse=True)
            the_new_resource = resource.pop(0)
        if step_number == 5:
            # New cards are at the end of the list
            the_new_resource = resource.pop()


    # Return an attribute to display if its not blank.
    if path_for_attribute_to_display[0]:
        our_response["attribute_to_display"] = get_data_on_attribute_path(the_new_resource, path_for_attribute_to_display)
    # Remember an attribute of the new resource if its not blank.
    if path_for_attribute_to_remember[0]:
        our_response["attribute_to_remember"] = get_data_on_attribute_path(the_new_resource, path_for_attribute_to_remember)
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
        time.sleep(2)
        timer = timer + 2
        resource = current_user.make_authorized_request(third_party_service, resource_url)
        resource = resource.json()
        if len(resource) == 0: # If empty list, it doesn't exist
            return json.dumps(our_response)
        for key in path_for_attribute_to_display:
            key = autoconvert(key)
            if type(resource) == list and type(key) == int:
                resource = resource[key]
            elif key in resource:
                resource = resource[key]
            else: # key doesn't exist
                return json.dumps(our_response)
        # If resource is still a dict, we didn't find what we were looking for.
        if type(resource) != dict:
            our_response["attribute_exists"] = True
            our_response["attribute_to_display"] = resource
            our_response["timeout"] = False
            return json.dumps(our_response)
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
        time.sleep(2)
        timer = timer + 2
        resource = current_user.make_authorized_request(third_party_service, resource_url)
        resource = resource.json()
        trigger_check = get_data_on_attribute_path(resource, trigger_checks)
        trigger_value = autoconvert(trigger_value)
        if trigger_check == trigger_value:
            our_response["attribute_value_matches"] = True
            our_response["attribute_to_display"] = get_data_on_attribute_path(resource,path_for_attribute_to_display)
            our_response["timeout"] = False
            return json.dumps(our_response)
    return json.dumps(our_response)

@app.route("/check_attribute_for_update", methods=['POST'])
def check_attribute_for_update():
    # Check once for original_value of attribute
    # then check if attribute value has changed
    # Return that endpoint

    # Require Authorization header for this endpoint
    if 'Authorization' in request.headers:
        htc_access = request.headers['Authorization']
    else:
        response['error'] = 'Authorization required'
        return make_response(response, 403)

    our_response = {
        "original_attribute_value" : False,
        "attribute_value_updated" : False,
        "attribute_to_display" : False,
        # "attribute_to_remember" : False,
        "timeout" : True
    }

    current_user = Bf_user.query.filter_by(access_token=htc_access).first()

    third_party_service = request.form['thirdPartyService']
    resource_url = request.form['currentStep[triggerEndpoint]']
    if 'rememberedAttribute' in request.form:
        remembered_attribute = request.form['rememberedAttribute']
    try:
        resource_url = resource_url.replace('replace_me',remembered_attribute)
    except:
        pass
    path_for_attribute_to_check = request.form['currentStep[triggerCheck]'].split(',')
    # trigger_value = request.form['currentStep[triggerValue]']
    # Dispaly same column we were checking
    path_for_attribute_to_display = request.form['currentStep[triggerCheck]'].split(',')
    # path_for_attribute_to_remember = request.form['currentStep[thingToRemember]'].split(',')
    original_attribute_values = autoconvert(request.form['originalAttributeValues'])
    
    if not original_attribute_values:
        original_attribute_values = []
        response = current_user.make_authorized_request(third_party_service, resource_url)
        resources = response.json()
        for resource in resources:
            resource = get_data_on_attribute_path(resource, path_for_attribute_to_check)
            original_attribute_values.append(resource)
        our_response["original_attribute_values"] = original_attribute_values
        our_response["timeout"] = False
        return json.dumps(our_response)

    timer = 0
    while timer < 60:
        time.sleep(2)
        timer = timer + 2
        resource = current_user.make_authorized_request(third_party_service, resource_url)
        resources = resource.json()
        current_attribute_values = set()
        for resource in resources:
            current_attribute_values.add(get_data_on_attribute_path(resource, path_for_attribute_to_check))
        updated_value = current_attribute_values.difference(set(original_attribute_values))  
        # for resource in resources:
        #     if updated_value == resource["name"]:
        #         updated_value_id = resource["id"]
        if len(updated_value):
            updated_value = updated_value.pop()
            our_response["attribute_value_updated"] = True
            our_response["attribute_to_display"] = updated_value
            # our_response["attribute_to_remember"] = updated_value_id
            our_response["timeout"] = False
            return json.dumps(our_response)
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
        our_response["attribute"] = get_data_on_attribute_path(resource, path_for_attribute)
    except KeyError:
        pass
    try:
        our_response["attribute_2"] = get_data_on_attribute_path(resource, path_for_attribute_2)
    except KeyError:
        pass
    try:
        our_response["attribute_3"] = get_data_on_attribute_path(resource, path_for_attribute_3)
    except KeyError:
        pass
    return json.dumps(our_response)


@app.route('/signup', methods=['POST'])
def htc_signup():
    user_email = request.form['email'].lower()
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

    # EMail the new user
    subject = "Welcome to BizFriend.ly"
    html = '<h3>Thanks for joining, <a href="http://bizfriend.ly">BizFriend.ly</a>!</h3>'
    html += '<p>We\'re a community of entrepreneurial learners and teachers who share the latest digital skills and web services to run your business.</p>' 
    html += "<p>Now that you have an account, there's a few things you can do:</p>"
    html += '<ul><li>Start Learning! Try out a few lessons at <a href="http://bizfriend.ly/learn.html">http://bizfriend.ly/learn.html</a></li>'
    html += '<li>Start Teaching! Teach other business owners the skills you\'re best at <a href="http://bizfriend.ly/teach.html">http://bizfriend.ly/teach.html</a></li>'
    html += "<li>See all what other businesses are up to and track your accomplishments <a href=\"http://bizfriend.ly/connect.html\">http://bizfriend.ly/connect.html</a></li></ul>"
    html += "<p>We'd love to hear any feedback you have at <a href=\"http://bit.ly/1bS1yEQ\">http://bit.ly/1bS1yEQ</a> and feel free to email us with any questions!</p>"
    html += '''Andew & Ariel<br/>
               Co-Founders of <a href="http://bizfriend.ly">BizFriend.ly</a><br/>
               2013 Code for America Fellows<br/>
               <a href="mailto:kansascity@codeforamerica.org">kansascity@codeforamerica.org</a>
            '''

    requests.post(
        "https://api.mailgun.net/v2/app14961102.mailgun.org/messages",
        auth=("api", app.config['MAIL_GUN_KEY']),
        data={"from": "Andrew Hyder <andrewh@codeforamerica.org>",
              "to": [user_email],
              "subject": subject,
              "html": html})

    current_user = Bf_user.query.filter_by(email=user_email).first()
    response['access_token'] = current_user.access_token 
    response['email'] = current_user.email
    response['name'] = current_user.name
    response['id'] = current_user.id
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
        response['id'] = current_user.id
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
    for lesson in current_user.lessons_completed:
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
        current_user.lessons_completed.append(user_less)
        db.session.commit()
        response['status'] = 200
    else:
        response['status'] = 404
        response['error'] = "Unable to save lesson state."

    response = make_response(json.dumps(response), response['status'])
    response.headers['content-type'] = 'application/json'
    return response

@app.route('/third_party_services', methods=['GET','POST'])
def third_party_services():
    files = os.listdir('bizfriendly/static')
    response = []
    # third_party_service_resources = []
    for filename in files:
        json_data=open('bizfriendly/static/'+filename).read()
        data = json.loads(json_data)
        response.append(data)
    return json.dumps(response)

@app.route('/image_upload', methods=['POST'])
def image_upload():
    try:
        os.mkdir('tmp')
    except Exception as e:
        pass
    file = request.files['files[]']
    file.save(os.path.join('tmp', file.filename))

    # # Check image size
    # img = Image.open("tmp/"+file.filename)
    # # get the image's width and height in pixels
    # width, height = img.size
    # if width > 260:
    #     response = {}
    #     response["message"] = "Image too wide."
    #     return make_response(json.dumps(response), 401)

    conn = boto.connect_s3(app.config['AWS_ACCESS_KEY_ID'], app.config['AWS_SECRET_ACCESS_KEY'])
    mybucket = conn.get_bucket(app.config['S3_BUCKET_NAME'])
    k = Key(mybucket)
    k.key = file.filename
    k.set_contents_from_filename(os.path.join('tmp', file.filename))
    mybucket.set_acl('public-read', file.filename)
    conn.close()
    return_json = {
        "name": file.filename,
        "size": os.stat('tmp/'+file.filename).st_size,
        "url": "https://%s.s3.amazonaws.com/%s" % (app.config['S3_BUCKET_NAME'], file.filename)
    }
    return json.dumps({"files" : [return_json]})


@app.route('/request_password_reset', methods=['POST'])
def request_password_reset():
    email = request.form['email']

    # Validate emails
    if not re.match("^[a-zA-Z0-9_.+-]+\@[a-zA-Z0-9-]+\.+[a-zA-Z0-9]{2,4}$", email):
        response = {}
        response['error'] = 'That email doesn\'t look right.'
        response = make_response(json.dumps(response), 401)
        response.headers['content-type'] = 'application/json'
        return response

    # Get that user
    current_user = Bf_user.query.filter_by(email=email).first()
    current_user.reset_token = random.randrange(0,100000000)
    db.session.commit()

    subject = "Reset BizFriendly Password"
    text = "Want to change your BizFriend.ly password?"
    text += "http://bizfriend.ly/reset-password.html?"+str(current_user.reset_token)
    response = requests.post(
        "https://api.mailgun.net/v2/app14961102.mailgun.org/messages",
        auth=("api", app.config['MAIL_GUN_KEY']),
        data={"from": "Andrew Hyder <andrewh@codeforamerica.org>",
              "to": [email],
              "subject": subject,
              "text": text})
    return response.text

@app.route('/password_reset', methods=['POST'])
def password_reset():
    email = request.form['email']
    password = request.form['password']
    reset_token = request.form['resetToken']
    response = {}

    # Validate emails
    if not re.match("^[a-zA-Z0-9_.+-]+\@[a-zA-Z0-9-]+\.+[a-zA-Z0-9]{2,4}$", email):
        response['error'] = 'That email doesn\'t look right.'
        response = make_response(json.dumps(response), 401)
        return response

    # Reset password
    current_user = Bf_user.query.filter_by(email=email).first()
    if current_user.reset_token == int(reset_token):
        current_user.password = current_user.pw_digest(password)
        current_user.reset_token = None
        db.session.commit()

    response['message'] = "Password reset"
    response['status'] = 200
    response = make_response(json.dumps(response))
    response.headers['content-type'] = 'application/json'
    return response