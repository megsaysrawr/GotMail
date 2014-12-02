# mailboxxx.py

from send_email import sendemail
from mail_authentication import mail_auth, spark_auth
from spyrk import SparkCloud
import arrow

class Mailroom(object):
    """Initialize with a list of mailbox objects."""
    def __init__(self, mailboxes):
        self.mailboxes = mailboxes

    def addmailbox(self, mailbox):
        """Input either a single mailbox or a list of mailboxes
        to add them to the mailroom's list of mailboxes"""
        input_type = type(mailbox)
        if input_type is list:
            self.mailboxes.extend(mailbox)
        elif input_type is Mailbox:
            self.mailboxes.append(mailbox)



        
class Mailbox(object):
    def __init__(self, owner, mb_num, sensor_num, core):
        self.owner = owner
        self.number = mb_num  # Mailbox number
        self.got_mail = False   #Boolean --yes mail\no mail
        self.sensor_num = str(sensor_num)   # Sensor number ('1', '2', ...)
        self.core = core    # Relevant spark core
        self.lastchecked = None
        self.lastnotification = None
        
    def __str__(self):
        return 'Mailbox %d belonging to %s (on Core "%s")' % (self.number, self.owner.name, self.core.name)

    def check(self):
        """Checks mailbox for mail using sensor input """
        #self.got_mail = whatever we just found (Boolean)
        error = 0
        try:
            sensor = self.core.analogRead(self.sensor_num)
        except:
            #   Catch errors, spark temporarily disconnected from internet, etc.
            # print 'Connection error'
            error = 1
        else:
            if sensor > 2000:   # Mail threshold
                self.got_mail = True
            else:
                self.got_mail = False
            self.lastchecked = arrow.utcnow()
        return error

    def notify_yes(self):
        """Eventually, this will test the time passed since notify
        and then return True if we should send an email
        """
        return True

    def notify_owner(self, Owner):
        sendemail('OlinGotMail@gmail.com', self.owner.email, 'You\'ve Got Mail!', 'Go check your mailbox, ' + self.owner.name, \
             mail_auth['login'], mail_auth['password'])

class Owner(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        
def main():
    Olin = Mailroom([]) # Create a mailroom
    spark = SparkCloud(spark_auth['accesstoken'])  # Connect to Spark cloud
    
    steve = Owner('Steve', 'megan@mccauley.net', )
    steve_mail = Mailbox(steve, 128, 1, spark.RE_core1)

    Olin.addmailbox(steve_mail)
    ## Set schedule ##
    check_interval = 20 # Seconds
    check_sec = None
    while True: # Main loop
        current_time = arrow.utcnow()
        current_second = current_time.second
        if current_second % check_interval == 0 and check_sec != current_second:  # If its time to check for mail and we haven't already checked this second,
            check_sec = current_second
            print 'Checking mailboxes...'
            for mb in Olin.mailboxes:   # Go to every mailbox,
                error = mb.check()      # And check for mail
                if error:   # Fiddlesticks
                    print 'Error while checking ' + str(mb)
            print 'Done Checking.'

        # For every mailbox
            #if it's got mail AND NOT within




    # # if steve_mail.check() == True and steve_mail.notify_yes() == True:
    # #     steve_mail.notify_owner(steve)

if __name__ == '__main__':
    main()
