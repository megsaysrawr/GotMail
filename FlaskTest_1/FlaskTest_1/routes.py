from datetime import datetime
from flask import render_template, flash, redirect, request
from app import app
from forms import MailboxForm, LoginForm

import requests as reqs
import csv
import arrow


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/olin/mb<mbnum>', methods=['GET', 'POST'])
@app.route('/olin/<mbnum>', methods=['GET', 'POST'])
def home(mbnum=0):
    form = MailboxForm()
    if form.validate_on_submit():
        return redirect('/olin/'+str(form.num_box.data))
    def gotmail(mbnum):
        if mbnum == 0:
            return 'Please enter your mailbox url.'
        req = reqs.get('https://dl.dropboxusercontent.com/s/6lmwzacom7gdu0z/mailboxdata.csv')
        mbs = req.content.split()
        got_mail = mbs[mbnum - 1]
        responses = ["You've got mail!", "No mail today.", "This mailbox is not currently using Olin GotMail. Sign up!", "An error has occurred. Sorry!"]
        if got_mail == 'True':
            return responses[0]
        elif got_mail == 'False':
            return responses[1]
        elif got_mail == '""':
            return responses[2]
        else:
            return responses[3]
    msg = gotmail(int(mbnum))
    return render_template('index.html',
        timest = arrow.utcnow().replace(hours = -5).format('h:mm:ss A on dddd, M/D/YYYY'),
        title = 'Home Page',
        message = msg,
        form = form)

@app.route('/contact')
def contact():
    return render_template('contact.html',
        title = 'Contact',
        year = datetime.now().year,
        applicationname = 'Check Mail',
        message = 'Your contact page.')

@app.route('/about')
def about():
    return render_template('about.html',
        title = 'About',
        year = datetime.now().year,
        applicationname = 'Check Mail',
        message = 'Your application description page.')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', 
                           title='Sign In',
                           form=form)

