from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.admin import Admin, BaseView
from bizfriendly import app
from models import *
from forms import LoginForm
from flask import g, render_template, redirect, request, url_for
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required

# LOGIN --

# login manager
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login' 

# load login manager
@lm.user_loader
def load_user(id):
    return Bf_user.query.get(int(id))

# set global user to current user
@app.before_request
def before_request():
    g.user = current_user

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    # if the user is authenticated, go to the index page
    if g.user is not None and g.user.is_authenticated():
        return redirect('/api/admin/')
    else:
        if form.validate_on_submit():
            user = Bf_user.query.filter_by(email=form.email.data).first()
            login_user(user)
            return redirect('/api/admin/')

    return render_template('login.html',
            title = 'Sign In',
            form = form)

class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated()

# ADMIN ------------------------------------------------------------
admin = Admin(app, name='BizFriend.ly Admin', url='/api/admin')

class CategoryView(AdminView):
    column_display_pk = True

class ServiceView(AdminView):
    column_display_pk = True
    column_auto_select_related = True

class LessonView(AdminView):
    column_display_pk = True
    column_auto_select_related = True

class StepView(AdminView):
    column_display_pk = True
    column_auto_select_related = True
    # column_list = ('lesson_id','lesson','id','name','step_number','step_type','step_text','trigger_endpoint','trigger_check','trigger_value','thing_to_remember','feedback','next_step_number')
    # column_sortable_list = (('lesson_id',Lesson.id),'name','step_type')

class Bf_userView(AdminView):
    column_display_pk = True
    column_list = ('id','name','email','business_name','location','role')

class UserLessonView(AdminView):
    column_display_pk = True
    column_auto_select_related = True

admin.add_view(CategoryView(Category, db.session))
admin.add_view(CategoryView(Service, db.session))
admin.add_view(LessonView(Lesson, db.session))
admin.add_view(StepView(Step, db.session))
admin.add_view(Bf_userView(Bf_user, db.session))
admin.add_view(UserLessonView(UserLesson, db.session))
