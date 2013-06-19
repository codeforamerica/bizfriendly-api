import os, requests
from flask import Flask, render_template, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.restless
from flask.ext.heroku import Heroku
from flask_oauth import OAuth

#----------------------------------------
# initialization
#----------------------------------------

app = Flask(__name__)
heroku = Heroku(app) # Sets CONFIG automagically
db = SQLAlchemy(app)

# app.config.update(
#     DEBUG = True,
#     SQLALCHEMY_DATABASE_URI = 'postgres://hackyourcity@localhost/howtocity'
# )

#----------------------------------------
# models
#----------------------------------------

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    description = db.Column(db.Unicode)
    url = db.Column(db.Unicode)

    def __init__(self, name, description, url):
        self.name = name
        self.description = description
        self.url = url

    def __repr__(self):
        return '<Category %r>' % self.name

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    description = db.Column(db.Unicode)
    url = db.Column(db.Unicode)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __init__(self, name, description, url, category_id):
        self.name = name
        self.description = description
        self.url = url
        self.category_id = category_id

    def __repr__(self):
        return '<Lesson %r>' % self.name

class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    description = db.Column(db.Unicode)
    # url = db.Column(db.Unicode)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))

    def __init__(self, name, description, url):
        self.name = name
        self.description = description
        # self.url = url
        # self.lesson_id = lesson_id

    def __repr__(self):
        return '<Step %r>' % self.name


# Create the database tables.
if app.config['DEBUG']:

    db.drop_all()
    db.create_all()
    promote_online = Category('How to Promote Your Business Online', 'Lessons for promoting your business online.','promote_your_business_online')
    beyond_cash = Category('How to Bring Your Business Beyond Cash Only', 'Lessons for bringing your business beyond cash only.','beyond_cash_only')
    how_to_city_better = Category('How to better live in the city', 'Lessons for using the internet to make living in the city easier and more fun.','how_to_city_better')
    fb_page_lesson = Lesson('How to create Facebook Page', 'Lesson on how to create a Facebook Page.','facebook_page', 1)
    twitter_lesson = Lesson('How to create a Twitter Account', 'Lesson on how to create a Twitter account.','twitter_account', 1)
    yelp_lesson = Lesson('How to use Yelp', 'Lessons for how to use Yelp','how_to_yelp', 3)

    db.session.add(promote_online)
    db.session.add(beyond_cash)
    db.session.add(how_to_city_better)
    db.session.commit()
    db.session.add(fb_page_lesson)
    db.session.add(twitter_lesson)
    db.session.add(yelp_lesson)
    db.session.commit()

db.create_all()

# Create the Flask-Restless API manager.
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(Category, methods=['GET', 'POST', 'DELETE'], url_prefix='/api/v1', collection_name='categories')
manager.create_api(Lesson, methods=['GET', 'POST', 'DELETE'], url_prefix='/api/v1', collection_name='lessons')
manager.create_api(Step, methods=['GET', 'POST', 'DELETE'], url_prefix='/api/v1', collection_name='steps')

#----------------------------------------
# controllers
#----------------------------------------

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/categories")
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

@app.route("/category/<category_url>")
def category(category_url):
    # Get the correct lessons for this category
    category = Category.query.filter_by(url=category_url).first()
    lessons = Lesson.query.filter_by(category_id=category.id).all()
    return render_template('lessons.html', category=category, lessons=lessons, )

@app.route("/category/<category_url>/lesson/<lesson_url>")
def lesson(category_url, lesson_url):
    category = Category.query.filter_by(url=category_url).first()
    lesson = Lesson.query.filter_by(url=lesson_url).first()
    return render_template('lesson.html', category=category, lesson=lesson)

@app.route("/category/<category_url>/lesson/<lesson_url>/instructions/<instructions_url>")
def instructions(category_url, lesson_url, instructions_url):
    category = Category.query.filter_by(url=category_url).first()
    lesson = Lesson.query.filter_by(url=lesson_url).first()
    return render_template(instructions_url+'.html', category=category, lesson=lesson)

#----------------------------------------
# launch
#----------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
