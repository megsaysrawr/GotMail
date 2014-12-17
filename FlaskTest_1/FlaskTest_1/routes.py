from datetime import datetime
from flask import render_template, flash, redirect, Response
from app import app
from forms import LoginForm
from spark import sparkcheck
from urllib2 import urlopen

@app.route('/')
@app.route('/home')
def home():
    def gotmail():
        with open('
    return render_template(
        'index.html',
        title = 'Home Page',
        message = 'Message goes here!',
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

@app.route('/yieldit')
def yieldit():
    def inner():
        return 'Yes'
    return render_template(
        'index.html',
        title = 'Home Page',
        message = inner())  # text/html is required