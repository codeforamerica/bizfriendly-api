from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from models import Bf_user
from datetime import date

from bizfriendly import app

class LoginForm(Form):
    email = TextField()
    password = PasswordField()

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        if not Form.validate(self):
            return False

        user = Bf_user.query.filter_by(email=self.email.data).first()
        if user is None:
            self.email.errors.append('Unknown email')
            return False

        if not user.check_pw(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        if user.role != 'admin':
            self.email.errors.append('Not an admin.')
            return False

        self.user = user
        return True