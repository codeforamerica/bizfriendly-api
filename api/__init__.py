from flask import Flask
import flask.ext.restless
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqlamodel import ModelView
from howtocity import app, db
from models import *


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
    # column_select_related_list = (Category.id)

class StepView(ModelView):
	column_display_pk = True
	column_auto_select_related = True
	# column_select_related_list = (Category.id)
	# column_select_related_list = (Lesson.id)

admin.add_view(CategoryView(Category, db.session))
admin.add_view(LessonView(Lesson, db.session))
admin.add_view(StepView(Step, db.session))