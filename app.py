import os, requests
from flask import Flask, render_template, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.restless
from flask.ext.heroku import Heroku

#----------------------------------------
# initialization
#----------------------------------------

app = Flask(__name__)
heroku = Heroku(app) # Sets CONFIG automagically
db = SQLAlchemy(app)

app.config.update(
    DEBUG = True,
)

#----------------------------------------
# database
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
    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __init__(self, name, description, url):
        self.name = name
        self.description = description
        self.url = url
        # self.category_id = category_id

class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    description = db.Column(db.Unicode)
    url = db.Column(db.Unicode)
    # lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))

    def __init__(self, name, description, url):
        self.name = name
        self.description = description
        self.url = url
        # self.lesson_id = lesson_id


# Create the database tables.
if app.config['DEBUG']:
    db.drop_all()
    db.create_all()
    promote_online = Category('How to Promote Your Business Online', 'Lessons for promoting your business online.','category/promote_your_business_online')
    beyond_cash = Category('How to Bring Your Business Beyond Cash Only', 'Lessons for bringing your business beyond cash only.','category/beyond_cash_only')
    fb_page_lesson = Lesson('How to create Facebook Page', 'Lesson on how to create a Facebook Page.','facebook_page')
    twitter_lesson = Lesson('twitter_account', 'Lesson to create a Twitter account.','twitter_account')

    db.session.add(promote_online)
    db.session.add(beyond_cash)
    db.session.add(fb_page_lesson)
    db.session.add(twitter_lesson)
    db.session.commit()

db.create_all()

# Create the Flask-Restless API manager.
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(Category, methods=['GET', 'POST', 'DELETE'])
manager.create_api(Lesson, methods=['GET', 'POST', 'DELETE'])
manager.create_api(Step, methods=['GET', 'POST', 'DELETE'])

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

@app.route("/fb_page_instructions.html")
def fb_page_instructions():
    return render_template('fb_page_instructions.html')

@app.route("/categories")
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

@app.route("/category/<category>")
def category(category):
    return render_template(category+'.html')


#----------------------------------------
# launch
#----------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
