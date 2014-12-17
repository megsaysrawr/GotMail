from flask.ext.wtf import Form, html5
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, NumberRange

class MailboxForm(Form):
    num_box = html5.IntegerField('Mailbox Number', NumberRange(1, 10, 'Please enter your mailbox number (1-10)'))