# Merias-Social-Media-Text-Annotator
 
Meria's Annotator for social media text samples was created as a part of scientific work of thesis. 
It was created by Merja Kreivi-Kauppinen (2021-2022) at University of Oulu.
Meria's Annotator facilitates manual hate speech labeling process.

The code package of Social Media Text Annotator API needs following python library packages:

Flask, pysqlite3, Flask-sqlalchemy, flask-restful, pytest, pytest-cov, Flask-Script, Flask-Migrate, Pillow, jsonschema, requests, pandas

In order run Meria's Annotator flask API set up virtual environment, 
activate virtual environment, set flask, init database and populate database.

Activate created python virtual environment (on cmd):
    
    cd C:\GIT\Repositories\Social-Media-Text-Annotator\.venv\Scripts
    activate.bat

    c:/GIT/Repositories/Social-Media-Text-Annotator/.venv/Scripts/activate.bat

Go to ImageAnnotator folder: (provide 'cd ..' on cmd)
    (.venv) C:\GIT\Repositories\Social-Media-Text-Annotator>

Set cofiguration setting class as 'development' or 'production' or 'default' or 'testing'
    (.venv) C:\GIT\Repositories\Social-Media-Text-Annotator>set FLASK_ENV=development

In order to start the server set the package name 'hub' and run Flask in the hub folder:
    (.venv) C:\GIT\Repositories\Social-Media-Text-Annotator>set FLASK_APP=hub

--------------------

Init flask database basedir hub:
    (.venv) C:\GIT\Repositories\Social-Media-Text-Annotator>flask init-db

Populate flask database:
    (.venv) C:\Social-Media-Text-Annotator\HateSpeechAnnotator>flask populate-db

Flask populate-deb command creates database models, and populates User, TextContent, and TextAnnotation models.

API downloads excel file

--------------------

Run flask local host at http://localhost:5000/admin/

    (.venv) C:\Social-Media-Text-Annotator\HateSpeechAnnotator>flask run

