Olin GotMail
=======
Olin GotMail is a system for alerting recipients to physical mail in their on-campus mailboxes. Please visit our [website](https://megsaysrawr.github.io/GotMail "Project website") for more information. This repository contains our mail-checking script, `mail_main.py` and a `Flask-App` directory which holds files in support of a web application.

## Required modules:
- Arrow--A module for dates and times. `pip install arrow`
- Dropbox SDK--Dropbox's module for manipulating files within their cloud service. `pip install dropbox`
- Spyrk--A python wrapper of the Spark Core API. `pip install spyrk`
- Please see `requirements.txt` in the `Flask-App` directory to find modules required to run the web-app. 

## Authentication
In order to run these programs, you must create a file called `mail_authentication.py` in the project's root directory and structure it as shown in `mail_authentication_sample.py`. This handles authentication with the Spark Cloud, with GMail, and with Dropbox.

## Run
In order to monitor mailboxes, first configure your mailroom in and then run `mail_main.py`. Support functions are contained within `send_email.py` and `dropboxcsv.py`.
`mailboxdata.csv` is a sample of the data file stored in Dropbox.

## Flask
The `Flask-App` directory contains the resources necessary to create a web application which checks the status of a given mailbox. You will need to create a virtual environment and install modules to run this locally, but there is a `requirements.txt` in the [root directory](https://github.com/megsaysrawr/GotMail/tree/master/Flask-App/FlaskTest_1 "App root directory") of the app which lists all necessary modules.

## Spark Core
The script which runs on the Spark Core is avaliable in the `Spark Core` directory. This code reads sensors, exposes a function to the Spark Cloud and its web API, and blinks a indicator LED.

##Other directories
The `Renders` directory contains CAD renders of our sensor mount and mailbox.

The `Tests & Experimentation` directory contains scripts used to test concepts as well as older versions of the code that has now become `mail_main.py`.

