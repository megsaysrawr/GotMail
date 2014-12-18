## mail_authentication_sample.py ##

# To run the files in this repository, fill in the <VALUE> placeholders with 
# the requested access tokens or credientials. Save this authentication file 
# as "mail_authentication.py".

mail_auth = {'login' : '<YOUR-GMAIL-ACCOUNT>', 'password': '<YOUR-GMAIL-PASSWORD'}

spark_auth = {'accesstoken': '<SPARK-CLOUD-ACCESS-TOKEN>'}
# The above grants access to all Spark Core devices connected
# to the associated account.

dropbox_auth = {'accesstoken': '<DROPBOX-APP-ACCESS-TOKEN>'}
# Because we use the same dropbox account for all of our calls,
# we opt not to use Dropbox's OAuth authentication flow.
