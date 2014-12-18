from datetime import datetime
from flask import render_template, redirect
from app import app
from forms import MailboxForm
import requests as reqs
import csv
import arrow

# Every mailbox has urls which can directly access it's status.
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/olin/mb<mbnum>', methods=['GET', 'POST'])
@app.route('/olin/<mbnum>', methods=['GET', 'POST'])
def home(mbnum=0):
    if int(mbnum) > 10: # Error checking. No error if mailbox number is out-of-range.
        mbnum = 0
    form = MailboxForm()
    if form.validate_on_submit():
        return redirect('/olin/'+str(form.num_box.data))
    def gotmail(mbnum):
        if int(mbnum) == 0:
            return 'Please enter your mailbox number below.'
        req = reqs.get('https://dl.dropboxusercontent.com/s/6lmwzacom7gdu0z/mailboxdata.csv')
        mbs = req.content.split()
        got_mail = mbs[mbnum - 1]
        responses = ["You've got mail!", "There's no mail now.", "This mailbox is not currently using Olin GotMail. Sign up!", "An error has occurred. Sorry!"]
        if got_mail == 'True':  # If mailbox has mail
            return responses[0]
        elif got_mail == 'False':   # If mailbox has no mail
            return responses[1]
        elif got_mail == '""':  # If mailbox is not monitored
            return responses[2]
        else:                   # Something is wrong.
            return responses[3] 
    msg = gotmail(int(mbnum))
    if int(mbnum) == 0: # Start page message.
        statusm = 'Check your mailbox...'
    else:   # Give mailbox number on its page
        statusm = 'Current status of mailbox #%d:' % int(mbnum)
    return render_template('index.html',
        timest = arrow.utcnow().replace(hours = -5).format('h:mm:ss A on dddd, M/D/YYYY'),
        title = 'Home Page',
        statusmessage = statusm,
        message = msg,
        form = form)

@app.route('/about')
def about():
    return render_template('about.html')
