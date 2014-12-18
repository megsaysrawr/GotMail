#!C:\Users\reggert\Documents\Github_Virtualenvs\flaskenv1\Scripts\python.exe
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
from routes import *

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app

if __name__ == '__main__':
    import os
    host = os.environ.get('SERVER_HOST', 'localhost')
    try:
        port = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        port = 5555
    app.run(host, port)
