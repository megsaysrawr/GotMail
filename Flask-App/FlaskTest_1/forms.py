from flask.ext.wtf import Form, html5
from wtforms import StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class MailboxForm(Form):
    num_box = IntegerField('Mailbox Number', [NumberRange(min=1, max=10, message='Please enter your mailbox number (1-10)')])
    remember_me = BooleanField('remember_me', default=False)
