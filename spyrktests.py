# spyrktests.py

from spyrk import SparkCloud
from spyrk_config import authentication
from time import sleep

spark = SparkCloud(authentication['accesstoken'])

print spark.devices     # List all avaliable spark cores (dictionary with names). We have one. 

core = spark.RE_core1
print core.variables  # Dictionary of all exposed variable (names) and their types

print core.testinteger
print core.testString


for i in xrange(1000):
    # print core.blink
    print core.analogRead()
    sleep(.5)

