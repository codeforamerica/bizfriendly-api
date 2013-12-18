from flask.ext.sqlalchemy import SQLAlchemy
import hashlib, requests, os
from bizfriendly import app

db = SQLAlchemy(app)

#----------------------------------------
# models
#----------------------------------------

class Category(db.Model):
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False, unique=True)
    description = db.Column(db.Unicode)
    state = db.Column(db.Unicode)
    created_dt = db.Column(db.DateTime(), default=db.func.now())
    # Realtionships
    creator_id = db.Column(db.Integer, db.ForeignKey('bf_user.id'))
    creator = db.relationship('Bf_user', backref=db.backref('categories', lazy='dynamic'))

    def __init__(self, name=None, description=None, state=None, creator_id=None):
        self.name = name
        self.description = description
        self.state = state
        self.creator_id = creator_id

    def __repr__(self):
        return self.name

class Service(db.Model):
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False, unique=True)
    url = db.Column(db.Unicode)
    icon = db.Column(db.Unicode)
    short_description = db.Column(db.Unicode)
    long_description = db.Column(db.Unicode)
    additional_resources = db.Column(db.Unicode)
    tips = db.Column(db.Unicode)
    media = db.Column(db.Unicode)
    state = db.Column(db.Unicode)
    created_dt = db.Column(db.DateTime(), default=db.func.now())
    # Relationships
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('services', lazy='dynamic'))
    creator_id = db.Column(db.Integer, db.ForeignKey('bf_user.id'))
    creator = db.relationship('Bf_user', backref=db.backref('services', lazy='dynamic'))

    def __init__(self, category_id=None, name=None, url=None, icon=None, description=None, long_description=None, short_description=None, additional_resources=None, tips=None, media=None, state=None, creator_id=None ):
        self.name = name
        self.url = url
        self.icon = icon
        self.long_description = long_description
        self.short_description = short_description
        self.additional_resources = additional_resources
        self.tips = tips
        self.media = media
        self.state = state
        self.category_id = category_id
        self.creator_id = creator_id

    def __repr__(self):
        return self.name

class Lesson(db.Model):
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False, unique=True)
    description = db.Column(db.Unicode)
    ease = db.Column(db.Unicode)
    state = db.Column(db.Unicode)
    created_dt = db.Column(db.DateTime(), default=db.func.now())
    # Relationships
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    service = db.relationship('Service', backref=db.backref('lessons', lazy='dynamic'))
    creator_id = db.Column(db.Integer, db.ForeignKey('bf_user.id'))
    creator = db.relationship('Bf_user', backref=db.backref('lessons', lazy='dynamic'))

    def init(self, name=None, description=None, ease=None, state=None, service_id=None, creator_id=None):
        self.name = name
        self.description = description
        self.ease = ease
        self.state = state
        self.service_id = service_id
        self.creator_id = creator_id

    def __repr__(self):
        return self.name

class Step(db.Model):
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    step_type = db.Column(db.Unicode)
    step_number = db.Column(db.Integer, nullable=False)
    step_text = db.Column(db.Unicode)
    trigger_endpoint = db.Column(db.Unicode)
    place_in_collection = db.Column(db.Unicode)
    trigger_check = db.Column(db.Unicode)
    trigger_value = db.Column(db.Unicode)
    thing_to_remember = db.Column(db.Unicode)
    feedback = db.Column(db.Unicode)
    next_step_number = db.Column(db.Integer)
    created_dt = db.Column(db.DateTime(), default=db.func.now())
    # Relationships
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    lesson = db.relationship('Lesson', backref=db.backref('steps', lazy='dynamic'))
    creator_id = db.Column(db.Integer, db.ForeignKey('bf_user.id'))

    def __init__(self, step_number=None, step_type=None, step_text=None, trigger_endpoint=None, place_in_collection=None, trigger_check=None, trigger_value=None, thing_to_remember=None, feedback=None, next_step_number=None, lesson_id=None, creator_id=None):
        self.step_number = step_number
        self.step_type = step_type
        self.step_text = step_text
        self.trigger_endpoint = trigger_endpoint
        self.place_in_collection = place_in_collection
        self.trigger_check = trigger_check
        self.trigger_value = trigger_value
        self.thing_to_remember = thing_to_remember
        self.feedback = feedback
        self.next_step_number = next_step_number
        self.lesson_id = lesson_id
        self.creator_id = creator_id

class Bf_user(db.Model):
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Unicode, nullable=False, unique=True)
    password = db.Column(db.Unicode, nullable=False)
    access_token = db.Column(db.Unicode, nullable=False)
    name = db.Column(db.Unicode, nullable=False)
    business_name = db.Column(db.Unicode, nullable=True)
    location = db.Column(db.Unicode, nullable=True)
    reset_token = db.Column(db.BigInteger, nullable=True)
    role = db.Column(db.Unicode, nullable=True)
    created_dt = db.Column(db.DateTime(), default=db.func.now())
    # Relations
    lessons_completed = db.relationship("UserLesson")
    lessons_created = db.relationship("Lesson")

    # TODO: Decide how strict this email validation should be
    # @validates('email')
    # def validate_email(self, key, address):
    #     pass

    def __init__(self, email=None, password=None, name=None, business_name=None, location=None, role=None):
        self.email = str(email)
        password = str(password)
        self.access_token = hashlib.sha256(str(os.urandom(24))).hexdigest()
        self.password = self.pw_digest(password)
        self.name = name
        self.business_name = business_name
        self.location = location
        self.role = "user"

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

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

class UserLesson(db.Model):
    # Attributes
    __tablename__ = 'user_to_lesson'
    recent_step_id = db.Column(db.Integer, db.ForeignKey('step.id'))
    recent_step_number = db.Column(db.Integer)
    start_dt = db.Column(db.DateTime(timezone=False))
    end_dt = db.Column(db.DateTime(timezone=False), nullable=True)
    completed = db.Column(db.Boolean)
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('bf_user.id'), primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), primary_key=True)
    lesson = db.relationship('Lesson')
    user = db.relationship('Bf_user')

    def __init__(self, start_dt=None, end_dt=None, recent_step_id=None, recent_step_number=None):
        self.recent_step_id = recent_step_id
        self.recent_step_number = recent_step_number
        self.start_dt = start_dt 
        self.end_dt = end_dt
        self.completed = False

    def __repr__(self):
        return "User_to_lesson user_id: %s, lesson_id: %s" % (self.user_id, self.lesson_id)

class Connection(db.Model):
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.Unicode)
    access_token = db.Column(db.Unicode)
    created_dt = db.Column(db.DateTime(), default=db.func.now())
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('bf_user.id'))
    user = db.relationship('Bf_user', backref=db.backref('connections', lazy='dynamic'))

    def __init__(self, service=None, access_token=None):
        self.service = service
        self.access_token = access_token

    def __repr__(self):
        return "Connection user_id: %s, service: %s" % (self.user_id, self.service)
