from howtocity import db

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
        return self.name

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    description = db.Column(db.Unicode)
    url = db.Column(db.Unicode)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category_relationship = db.relationship('Category', backref=db.backref('category', lazy='dynamic'))

    def __init__(self, name=None, description=None, url=None, category_id=None):
        self.name = name
        self.description = description
        self.url = url
        self.category_id = category_id

    def __repr__(self):
        return self.name

class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    description = db.Column(db.Unicode)
    url = db.Column(db.Unicode)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    lesson_relationship = db.relationship('Lesson', backref=db.backref('lesson', lazy='dynamic'))

    def __init__(self, name, description, url, lesson_id):
        self.name = name
        self.description = description
        self.url = url
        self.lesson_id = lesson_id

    def __repr__(self):
        return self.name