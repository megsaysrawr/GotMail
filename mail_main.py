#mail_main.py

from send_email import sendemail
from mail_authentication import mail_auth, spark_auth
from spyrk import SparkCloud
from dropboxcsv import csvtocloud
import arrow
import csv

class Mailroom(object):
    """Initialize with a list of mailbox objects."""
    def __init__(self, mailboxes, max_boxes=10):
        self.mailboxes = mailboxes
        self.max_boxes = max_boxes
        self.total_mailroom = None

    def addmailbox(self, mailbox):
        """Input either a single mailbox or a list of mailboxes
        to add them to the mailroom's list of mailboxes"""
        input_type = type(mailbox)
        if input_type is list:
            self.mailboxes.extend(mailbox)
        elif input_type is Mailbox:
            self.mailboxes.append(mailbox)

    def mailroom_boxes(self):
        """Creates an empty dictionary of all mailboxes in mailroom"""
        total_mailroom = {}
        for mailbox in range(self.max_boxes):
            total_mailroom[mailbox] = None
        self.total_mailroom = total_mailroom

    def mailroom_list(self):
        """Generates a csv file of all mailboxes in the mailroom and 
        puts it on Dropbox"""
        for mailbox in self.mailboxes:
            self.total_mailroom[mailbox.number-1] = mailbox.got_mail
        with open('sample_csv.csv', 'wb') as csvfile:
            filewrite = csv.writer(csvfile)
            for mailbox in range(self.max_boxes):
                row = self.total_mailroom[mailbox]
                filewrite.writerow([row])
        with open('sample_csv.csv', 'rb') as sendfile:
            csvtocloud(sendfile)
        
class Mailbox(object):
    """Creates a Mailbox object that can be put in the Mailroom class"""
    def __init__(self, owner, mb_num, sensor_num, core):
        self.owner = owner  # Owner object
        self.number = mb_num  # Mailbox number
        self.got_mail = False   #Boolean --yes mail\no mail
        self.sensor_num = str(sensor_num)   # Sensor number ('1', '2', ...)
        self.core = core    # Relevant spark core
        self.lastchecked = None # Timestamp of last time we checked mailbox
        self.lastnotification = None # Timestamp of last time we emailed owner.
        self.newmail = None     # Has mail been added to a previously empty mailbox?
        
    def __str__(self):
        """Returns a descriptive string including the mailbox number, it's owner, and the core
        to which it is connected.
        """
        return 'Mailbox %d belonging to %s (on Core "%s")' % (self.number, self.owner.name, self.core.name)

    def check(self):
        """Checks mailbox for mail using sensor input """
        error = 0
        try:
            sensor = self.core.analogRead(self.sensor_num)
        except:     # Specifically, KeyError, I think.
            # Catch errors, spark temporarily disconnected from internet, etc.
            # print 'Connection error'
            error = 1
        else:
            previous_mail = self.got_mail
            if sensor > 3300:   # Mail threshold
                self.got_mail = True
            else:
                self.got_mail = False
            if not previous_mail and self.got_mail: # If we didn't have mail, and now we do,
                # Then we should have new mail.
                self.newmail = True
                # If we decide to NOT send reminder emails, then we may need only this and no 
                # last notification time. This edge detection will send a notification once per 
                # 'set' of mail. 
                #
                # Then again, it may be good to keep the last notification time and use it to check
                # that our sensors aren't wigging out and spamming people with mail. 

            elif previous_mail and not self.got_mail:   # If we had mail and now we don't, 
                # Then they picked up their mail
                self.lastnotification = None    # Reset notification counter.
            
            else:
                self.newmail = False # If we have no mail OR had mail last time we checked,
                                     # then there is no new mail.

            self.lastchecked = arrow.utcnow()
        return error

    def notify_yes(self):
        """Eventually, this will test the time passed since notify
        and then return True if we should send an email POADS
        """
        if self.lastnotification is None:
            return True
        past = self.lastnotification
        present = arrow.utcnow()
        difference = present - past
        print difference
        if difference.seconds > 60:    # Configure this. Make mailbox attribute?
            return True
        return False

    def notify_owner(self):
        sendemail('OlinGotMail@gmail.com', self.owner.email, 'You\'ve Got Mail!', 'Go check your mailbox, ' + self.owner.name + '.', \
             mail_auth['login'], mail_auth['password'])
        self.lastnotification = arrow.utcnow()

class Owner(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        
def main():
    olin = Mailroom([]) # Create a mailroom
    spark = SparkCloud(spark_auth['accesstoken'])  # Connect to Spark cloud
    
    steve = Owner('Ryan', 'emailtestre@gmail.com')
    steve_mail = Mailbox(steve, 4, 1, spark.RE_core1)

    olin.addmailbox(steve_mail)
    olin.mailroom_boxes() # create empty dictionary of all mailboxes in mailroom
    ## Set schedule ##
    check_interval = 10 # Seconds
    check_sec = None
    while True: # Main loop
        current_time = arrow.utcnow()
        current_second = current_time.second
        if current_second % check_interval == 0 and check_sec != current_second:  # If its time to check for mail and we haven't already checked this second,
            check_sec = current_second
            print 'Checking mailboxes...'
            for mb in olin.mailboxes:   # Go to every mailbox,
                error = mb.check()      # And check for mail
                print mb.got_mail
                if error:   # Fiddlesticks
                    print 'Error while checking ' + str(mb)
            print 'Done Checking.'
            for mb in olin.mailboxes:
                if mb.got_mail and mb.notify_yes():
                    mb.notify_owner()
                    print 'SENT!'
            olin.mailroom_list() # loop and generate csv file and put on Dropbox

        # For every mailbox
            #if it's got mail AND NOT within a few days since last notification




    # # if steve_mail.check() == True and steve_mail.notify_yes() == True:
    # #     steve_mail.notify_owner(steve)

if __name__ == '__main__':
    main()
