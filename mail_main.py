#mail_main.py

from send_email import sendemail
from mail_authentication import mail_auth, spark_auth
from spyrk import SparkCloud
from dropboxcsv import csvtocloud
import arrow
import csv

class Mailroom(object):
    """A mailroom object contains many mailbox objects.
    Attributes:
    self.mailboxes is a list of mailbox objects. A mailbox
        object exists for every mailbox monitored by GotMail.
    self.max_boxes is an integer representing the number of 
        mailboxes in the physical mailroom.
    self.total_mailroom is a dictionary with key = mailbox number,
    value = mailbox status. This is created in the
    self.mailroom_boxes() method.
    """
    def __init__(self, mailboxes, max_boxes=10):
        """Initialize a mailroom with a list of mailbox objects.
        Optionally, give a maximum number of mailboxes; the default
        value is 10.
        """
        self.mailboxes = mailboxes
        self.max_boxes = max_boxes
        self.total_mailroom = None

    def addmailbox(self, mailbox):
        """Input either a single mailbox or a list of mailboxes
        to add them to the mailroom's list of mailboxes [self.mailboxes].
        """
        input_type = type(mailbox)
        if input_type is list:
            self.mailboxes.extend(mailbox)
        elif input_type is Mailbox:
            self.mailboxes.append(mailbox)

    def mailroom_boxes(self):
        """Creates an empty dictionary of all mailboxes in mailroom.
        """
        total_mailroom = {}
        for mailbox in range(self.max_boxes):
            total_mailroom[mailbox] = None
        self.total_mailroom = total_mailroom

    def mailroom_list(self):
        """Generates a csv file of all mailboxes in the mailroom and 
        places it on Dropbox.
        """
        for mailbox in self.mailboxes:
            self.total_mailroom[mailbox.number-1] = mailbox.got_mail
        with open('mailboxdata.csv', 'wb') as csvfile:
            filewrite = csv.writer(csvfile)
            for mailbox in range(self.max_boxes):
                row = self.total_mailroom[mailbox]
                filewrite.writerow([row])
        with open('mailboxdata.csv', 'rb') as sendfile:
            csvtocloud(sendfile)
        
class Mailbox(object):
    """Creates a Mailbox object that can be put in the Mailroom class.
    Attributes:
    self.owner is an owner object representing the owner of the mailbox.
    self.number is the number assigned to the physical mailbox.
    self.got_mail is a boolean value representing whether or not
        there is mail in the mailbox. [True => got mail, False => no mail].
    self.sensor_num relates to the Spark Core pin into which this mailbox's
        sensor is plugged in to. (e.g. Sensor number 1 is plugged into pin A0).
    self.core is a Spark Core object to which the mailbox's sensor is connected.
        This would allow us to scale to multiple Spark Cores.
    self.lastchecked is a timestamp of the last time we checked the status of
        the mailbox.
    self.lastnotification is a timestamp of the last time we sent an email to
        self.owner. This enables limiting the frequency of notifications. 
    self.newmail is a boolean value representing whether or not there is new
        mail in the mailbox (i.e. there was no mail, and now there is mail,
        ergo there is new mail.). [True => mail was added to a previously empty
        mailbox. False => there is no mail OR there already was existing mail].

    """
    def __init__(self, owner, mb_num, sensor_num, core):
        """
        """
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
            error = 1
        else:
            previous_mail = self.got_mail
            if sensor > 3012:   # Mail threshold
                self.got_mail = True
            else:
                self.got_mail = False
            if not previous_mail and self.got_mail: # If we didn't have mail, and now we do,
                # Then we should have new mail.
                self.newmail = True

            elif previous_mail and not self.got_mail:   # If we had mail and now we don't, 
                # Then they picked up their mail
                self.lastnotification = None    # Reset notification counter.
            
            else:
                self.newmail = False # If we have no mail OR had mail last time we checked,
                                     # then there is no new mail.

            self.lastchecked = arrow.utcnow()
        return error

    def notify_yes(self):
        """Based on the current time and self.lastnotification, decide whether
        to notify self.owner of the presence of mail.
        """
        if self.lastnotification is None:
            return True
        past = self.lastnotification
        present = arrow.utcnow()
        difference = present - past
        if difference.seconds > 172800: # 48 hours    
            return True
        return False

    def notify_owner(self):
        """Send an email to self.owner.
        """
        sendemail('OlinGotMail@gmail.com', self.owner.email, 'You\'ve Got Mail!', 'Please check your mailbox, ' + self.owner.name + '.', \
             mail_auth['login'], mail_auth['password'])
        self.lastnotification = arrow.utcnow()

class Owner(object):
    """An owner object represents the owner of the mailbox (i.e. the
        recipeint of mail).
        Attributes:
        self.name is the owner's name.
        self.email is the owner's email address.
    """
    def __init__(self, name, email):
        """Initialize with owner's name and email address
        """
        self.name = name
        self.email = email
        
def main():
    olin = Mailroom([]) # Create a mailroom
    spark = SparkCloud(spark_auth['accesstoken'])  # Connect to Spark cloud
    
    # Configure owners
    own_1 = Owner('Meg', 'Megan@McCauley.net')

    # Configure Mailboxes
    steve_mail = Mailbox(own_1, 4, 1, spark.RE_core1)

    # Configure Mailroom
    olin.addmailbox(steve_mail)

    olin.mailroom_boxes() # create empty dictionary of all mailboxes in mailroom
    ## Set schedule ##
    check_interval = 10 # Seconds
    check_sec = None
    while True: # Main loop
        current_time = arrow.utcnow()
        current_second = current_time.second
        if current_second % check_interval == 0 and check_sec != current_second:  
        # If it's time to check for mail and we haven't already checked this second,
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
            olin.mailroom_list() # generate csv file and put on Dropbox

if __name__ == '__main__':
    main()
