def sparkcheck():
    """Checks mailbox for mail using sensor input """
    sparkserv = SparkCloud('228c805ab8a49e38bef15082e48bd87307561b6d')  # Connect to Spark cloud
    core = sparkserv.RE_core1
    try:
        sensor = core.analogRead('1')
    except:     # Specifically, KeyError, I think.
        # Catch errors, spark temporarily disconnected from internet, etc.
        # print 'Connection error'
        got_mail_ret = 2
    else:
        if sensor > 3300:   # Mail threshold
            got_mail_ret = 1
        else:
            got_mail_ret = 0

    responses = ['There is no mail.', 'You\'ve got mail!', 'There was a connectivity error. Please try again later.']
    return responses[got_mail_ret]
