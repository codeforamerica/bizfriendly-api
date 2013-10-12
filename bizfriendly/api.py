import flask.ext.restless
from bizfriendly import app
from models import *

api_version = '/api/v1'

# API ------------------------------------------------------------
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)
columns = ['creator.password','creator.reset_token','creator.access_token','creator.role']
manager.create_api(Category, exclude_columns=columns, methods=['GET', 'POST', 'PUT'], url_prefix=api_version, collection_name='categories', max_results_per_page=-1)
manager.create_api(Service, exclude_columns=columns, methods=['GET', 'POST', 'PUT'], url_prefix=api_version, collection_name='services', max_results_per_page=-1)
manager.create_api(Lesson, exclude_columns=columns, methods=['GET', 'POST', 'PUT'], url_prefix=api_version, collection_name='lessons', max_results_per_page=-1)
manager.create_api(Step, exclude_columns=columns, methods=['GET', 'POST', 'PUT'], url_prefix=api_version, collection_name='steps', max_results_per_page=-1)
manager.create_api(Request, methods=['GET','POST', 'PUT'], url_prefix=api_version, collection_name='requests', max_results_per_page=-1)
columns = ['password','reset_token','access_token','role','connections.access_token']
manager.create_api(Bf_user, exclude_columns=columns,methods=['GET'], url_prefix=api_version, collection_name='users', max_results_per_page=-1)
columns = ['user.password','user.reset_token','user.access_token','user.role']
manager.create_api(UserLesson, exclude_columns=columns, methods=['GET'], url_prefix=api_version, collection_name='userlessons', max_results_per_page=-1)
manager.create_api(Rating, exclude_columns=columns, methods=['GET','POST', 'PUT'], url_prefix=api_version, collection_name='ratings', max_results_per_page=-1)
