from spyrk import SparkCloud
from mail_authentication import spark_auth, mail_auth
from time import sleep
from send_email import sendemail

spark = SparkCloud(spark_auth['accesstoken'])
core = spark.RE_core1

sensorvalue = core.analogRead()
# getsensorfunction()
print sensorvalue
if sensorvalue > 1500:
    sendemail(mail_auth['login'], '[EMAIL_TO]', 'You\'ve Got Mail!', 'Dear Valued Customer,\nYou\'ve got mail in your mailbox. You\'re very lucky.\nSincerely,\nme', mail_auth['login'], mail_auth['password'])
else:
    print "No mail for you!"