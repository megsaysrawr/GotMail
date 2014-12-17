import dropbox as dpb
from mail_authentication import dropbox_auth

def csvtocloud(file):
    """@file: file object"""
    client = dpb.client.DropboxClient(dropbox_auth['accesstoken'])
    client.put_file('/mailboxdata.csv', file, overwrite=True)



if __name__ == '__main__':
    with open('samplecsv.csv', 'r+b') as sampfile:
        csvtocloud(sampfile)