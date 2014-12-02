# spyrktests.py

from spyrk import SparkCloud
from mail_authentication import spark_auth
from time import sleep

spark = SparkCloud(spark_auth['accesstoken'])

print spark.devices     # List all avaliable spark cores (dictionary with names). We have one. 

core = spark.RE_core1
print core.variables  # Dictionary of all exposed variable (names) and their types

for i in xrange(1000):
    # print core.blink
    print core.analogRead('1')
    sleep(.5)

