# Meria's Annotator for Social Media Texts
# University of Oulu
# Created by Merja Kreivi-Kauppinen (2021-2022)

# Social-Media-Text-Annotator/HateSpeechAnnotator API

# This file is testing population of API database models

# populate_test_database.py

# ------------------------------------------------------------------------------------------

"""
In order to run this test code of ImageAnnotator flask API.

Add following files and folders to ImageAnnotator -folder:

* Data -folder - includes largeTestfile and smallTestfile

* this file 'populate_test_database.py' next to 'manage.py' -file

In order run HateSpeechAnnotator flask API and this file 
activate virtual environment, set flask, init database and populate database.

Activate created python virtual environment (on cmd):
    cd C:\Social-Media-Text-Annotator\HateSpeechAnnotator\.venv\Scripts
    activate.bat

Go to ImageAnnotator folder: (provide 'cd ..' on cmd)
    (.venv) C:\Social-Media-Text-Annotator\HateSpeechAnnotator>

Set cofiguration setting class as 'development' or 'production' or 'default' or 'testing'
    (.venv) C:\Social-Media-Text-Annotator\HateSpeechAnnotator>set FLASK_ENV=development

In order to start the server set the package name 'hub' and run Flask in the hub folder:
    (.venv) C:\Social-Media-Text-Annotator\HateSpeechAnnotator>set FLASK_APP=hub

Run test file by command:
    (.venv) C:\Social-Media-Text-Annotator\HateSpeechAnnotator>python populate_test_database.py
    # EI TOIMI !!!!!

TESTING
* This code creates database models, 
* and populates User, TextContent, TextAnnotation

RESULTS
* available at the end of the code

"""

from hub import create_app, db
from hub.models import User, TextAnnotation, TextContent

from datetime import datetime
import glob
import base64
from io import BytesIO
import os


config = os.getenv('FLASK_ENV')
print("configuration: ", config)

# -------------------------------------------------------------------
# creates app with defined environment and configuration
app = create_app(os.getenv('FLASK_ENV') or 'default')
with app.app_context():
    db.create_all()

# -------------------------------------------------------------------
# Testing User -model population

# Create new row for new user to database by using User -model
    user1 = User(user_name = "Meria Developer", userNick = "meria", user_password="mötkäle")
    user2 = User(user_name = "Ville Visitor", userNick = "vierailija", user_password="kukka")
    user3 = User(user_name = "Test Engineer", userNick = "testaaja", user_password="1234test")

# Add model to the session
    db.session.add_all([user1, user2, user3])

# Save session to database with commit
    db.session.commit()

    print("\nADD USER \n")

# Execute SQL query for database by using Model.query
# OR for db.session.query(Model)
# query.all() get all rows in the database as a list
    result_users = User.query.all()
    for item in result_users:
        print("User object: ", item ,"   User ID: ", item.id, "   Username:  ", item.user_name, "   User nick:  ", item.userNick, "   User password:  ", item.user_password)
