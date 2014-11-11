import smtplib
from mail_authentication import mail_auth

# http://www.pythonforbeginners.com/code-snippets-source-code/using-python-to-send-email

def sendemail(from_addr, to_addr_list, subject, message, login, password, smtpserver = 'smtp.gmail.com:587'):

	header = 'From: %s\n' % from_addr
	header += 'To: %s\n' % to_addr_list
	header += 'Subject: %s\n\n' % subject
	message = header + message

	server = smtplib.SMTP(smtpserver)
	server.starttls()
	server.login(login, password)
	problems = server.sendmail(from_addr, to_addr_list, message)
	server.quit

def main():
    sendemail('OlinGotMail@gmail.com', '[DEST_EMAIL]', 'You\'ve Got Mail!', 'Go check your mailbox, you lucky one you!',\
    mail_auth['login'], mail_auth['password'])

if __name__ == '__main__':
    main()
