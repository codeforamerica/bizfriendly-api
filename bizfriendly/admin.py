from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.admin import Admin
from bizfriendly import app
from models import *

# ADMIN ------------------------------------------------------------
admin = Admin(app, name='BizFriend.ly Admin', url='/api/admin')

class CategoryView(ModelView):
    column_display_pk = True

class ServiceView(ModelView):
    column_display_pk = True
    column_auto_select_related = True

class LessonView(ModelView):
    column_display_pk = True
    column_auto_select_related = True

class StepView(ModelView):
    column_display_pk = True
    column_auto_select_related = True
    # column_list = ('lesson_id','lesson','id','name','step_number','step_type','step_text','trigger_endpoint','trigger_check','trigger_value','thing_to_remember','feedback','next_step_number')
    # column_sortable_list = (('lesson_id',Lesson.id),'name','step_type')

# class Bf_userView(ModelView):
#     column_display_pk = True
#     column_auto_select_related = True

# class UserLessonView(ModelView):
#     column_display_pk = True
#     column_auto_select_related = True

class RatingView(ModelView):
    column_display_pk = True
    column_auto_select_related = True

admin.add_view(CategoryView(Category, db.session))
admin.add_view(CategoryView(Service, db.session))
admin.add_view(LessonView(Lesson, db.session))
admin.add_view(StepView(Step, db.session))
# admin.add_view(Bf_userView(Bf_user, db.session))
# admin.add_view(UserLessonView(UserLesson, db.session))
admin.add_view(RatingView(Rating,db.session))