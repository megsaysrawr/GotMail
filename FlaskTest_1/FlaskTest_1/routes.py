from datetime import datetime
from flask import render_template, flash, redirect
from app import app
from forms import LoginForm
from spark import sparkcheck

@app.route('/')
@app.route('/home')
def home():
    sparkserv = SparkCloud('accesstoken')  # Connect to Spark cloud
    core = sparkserv.RE_core1
    try:
        sensor = core.analogRead('1')
    except:     # Specifically, KeyError, I think.
        # Catch errors, spark temporarily disconnected from internet, etc.
        # print 'Connection error'
        got_mail_ret = 2
    else:
        if sensor > 3300:   # Mail threshold
            got_mail_ret = 1
        else:
            got_mail_ret = 0

    responses = ['There is no mail.', 'You\'ve got mail!', 'There was a connectivity error. Please try again later.']
    return render_template(
        'index.html',
        title = 'Home Page',
        message = responses[got_mail_ret],
    )

@app.route('/contact')
def contact():
    return render_template(
        'contact.html',
        title = 'Contact',
        year = datetime.now().year,
        applicationname = 'Check Mail',
        message = 'Your contact page.'
    )

@app.route('/about')
def about():
    return render_template(
        'about.html',
        title = 'About',
        year = datetime.now().year,
        applicationname = 'Check Mail',
        message = 'Your application description page.'
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/home')
    return render_template(
        'login.html', 
         title='Sign In',
         year = datetime.now().year,
         applicationname = 'Check Mail',
         message = 'Your application description page.',
         form=form)
    