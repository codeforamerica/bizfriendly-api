import flask.ext.restless
from bizfriendly import app
from models import *

api_version = '/api/v1'

# API ------------------------------------------------------------
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Category, methods=['GET', 'POST'], url_prefix=api_version, collection_name='categories', max_results_per_page=-1)
manager.create_api(Service, methods=['GET', 'POST'], url_prefix=api_version, collection_name='services', max_results_per_page=-1)
manager.create_api(Lesson, methods=['GET', 'POST'], url_prefix=api_version, collection_name='lessons', max_results_per_page=-1)
manager.create_api(Step, methods=['GET', 'POST'], url_prefix=api_version, collection_name='steps', max_results_per_page=-1)
columns = ['id','name','email']
manager.create_api(Bf_user, include_columns=columns,methods=['GET'], url_prefix=api_version, collection_name='users', max_results_per_page=-1)
columns = ['lesson','lesson.name','lesson.id','user','user.name','end_dt']
manager.create_api(UserLesson, include_columns=columns, methods=['GET'], url_prefix=api_version, collection_name='userlessons', max_results_per_page=-1)
manager.create_api(Rating, methods=['GET','POST'], url_prefix=api_version, collection_name='ratings', max_results_per_page=-1)