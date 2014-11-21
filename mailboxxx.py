# mailboxxx.py

from send_email import sendemail
from mail_authentication import mail_auth

class Mailbox(object):
	def __init__(self, owner, sensor_num):
		self.owner = owner
		self.got_mail = False	#Boolean --yes mail\no mail
		self.sensor_num = sensor_num

	def check(self):
		"""Checks mailbox for mail using sensor input """
		#self.got_mail = whatever we just found (Boolean)
		return True

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
		#self.box_num = box_num		# For scaling

def main():
	steve = Owner('Steve', 'megan@mccauley.net')
	steve_mail = Mailbox(steve, 1)
	if steve_mail.check() == True and steve_mail.notify_yes() == True:
		steve_mail.notify_owner(steve)

if __name__ == '__main__':
    main()
