import os, requests, json
from flask import render_template, send_from_directory, request
from howtocity import app

#----------------------------------------
# controllers
#----------------------------------------

def get_how_to_city_api_url():
    api_version = 'v1'
    url = request.url_root
    how_to_city_api_url = url+'api/'+api_version+'/'
    return how_to_city_api_url

def call_how_to_city_api(endpoint, column_name=None, operator=None, value=None, single=False):
    # Add in lots of testing
    how_to_city_api_url = get_how_to_city_api_url()
    how_to_city_api_url = how_to_city_api_url + endpoint
    headers = {'Content-Type': 'application/json'}
    if column_name and operator and value:
        filters = [dict(name=column_name, op=operator, val=value)]
        params = dict(q=json.dumps(dict(filters=filters, single=single)))
        response = requests.get(how_to_city_api_url, params=params, headers=headers)
    else:
        response = requests.get(how_to_city_api_url, headers=headers)
    response = response.json()
    try: 
        response = response['objects']
    except KeyError:
        pass
    return response

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/<category_url>")
def category(category_url):
    category = call_how_to_city_api(endpoint='categories',column_name='url',operator='==',value=category_url,single=True)
    lessons = call_how_to_city_api(endpoint='lessons',column_name='category_id', operator='==',value=category['id'])
    return render_template('lessons.html', category=category, lessons=lessons)

@app.route("/categories")
def categories():
    categories = call_how_to_city_api('categories')
    return render_template('categories.html', categories=categories)

@app.route("/lessons")
def lessons():
    categories = call_how_to_city_api('categories')
    lessons = call_how_to_city_api('lessons')
    return render_template('all_lessons.html', categories=categories,lessons=lessons)

@app.route("/<category_url>/<lesson_url>")
def lesson(category_url, lesson_url):
    category = call_how_to_city_api(endpoint='categories',column_name='url',operator='==',value=category_url,single=True)
    lesson = call_how_to_city_api(endpoint='lessons',column_name='url',operator='==',value=lesson_url,single=True)
    return render_template('lesson.html', category=category, lesson=lesson)

@app.route("/<category_url>/<lesson_url>/instructions/<instructions_url>", methods=['GET', 'POST'])
def instructions(category_url, lesson_url, instructions_url):
    category = call_how_to_city_api(endpoint='categories',column_name='url',operator='==',value=category_url,single=True)
    lesson = call_how_to_city_api(endpoint='lessons',column_name='url',operator='==',value=lesson_url,single=True)
    # steps = call_how_to_city_api(endpoint='steps',column_name='lesson_id',operator='==',value=lesson['id'])

    # Foursquare Instructions
    if instructions_url == 'foursquare_instructions':
        foursquare_auth_url = None
        access_token = None
        if 'code' in request.args:
            auth_code = request.args['code']
            # Get access_token
            access_token = foursquare_lesson.get_access_token(auth_code)
            user = foursquare_lesson.get_user_data(access_token)
            todo_count = foursquare_lesson.get_todo_count(access_token)
            return render_template(instructions_url+'.html', category=category, lesson=lesson, user=user, todos_count=todos_count)
        else:
            # Authorize
            foursquare_auth_url = foursquare_lesson.foursquare_oauth()
            return render_template(instructions_url+'.html', category=category, lesson=lesson, foursquare_auth_url=foursquare_auth_url)
    
    return render_template(instructions_url+'.html', category=category, lesson=lesson)

@app.route("/foursquare/venue/<venue_id>")
def get_venue(venue_id):
    venue = foursquare_lesson.venue_api(venue_id)
    venue = json.dumps(venue)
    return venue

@app.route("/foursquare/todo_count/<access_token>")
def get_todo_count():
    return 