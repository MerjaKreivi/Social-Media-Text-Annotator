## INSTALL, SET UP VENV, and RUN

## Getting started

It is recommended to use virtual environment for using and testing the code. 

The use of Python 3.7 or newer version is required. Use "pip install" to install virtual environment packages. 

The code package of Social Media Text Annotator API needs for example following python library packages:

<li>   Flask, pysqlite3, Flask-sqlalchemy, flask-restful, pytest, pytest-cov, Flask-Script, Flask-Migrate, Pillow, jsonschema, requests, pandas


## Set up python virtual environment for flask project

Open command prompt (cmd) and proceed to C root folder. Clone Social-Media-Text-Annotator project using following command. The command will create folder C:\Social-Media-Text-Annotator.

    C:\>git clone https://github.com/MerjaKreivi/Social-Media-Text-Annotator.git

Create virtual environment on Social-Media-Text-Annotator folder.

    C:\Social-Media-Text-Annotator\python -m venv .venv

Next activate created python virtual environment (on cmd):

    C:\Social-Media-Text-Annotator\.venv\Scripts>activate.bat


## Install required python libraries

Install packages defined at "requirements.txt" -file with following command in cmd:

    (.venv) C:\Social-Media-Text-Annotator>pip install -r requirements.txt

Install project with pip in editable (-e) mode with dot (.)

    (.venv) C:\Social-Media-Text-Annotator>pip install -e .


## Set up configuration for flask

In order run Meria's Annotator flask API set up virtual environment, 
activate virtual environment, set flask, init database and populate database.

Set configuration setting class as 'development' or 'production' or 'default' or 'testing'

    (.venv) C:\GIT\Repositories\Social-Media-Text-Annotator>set FLASK_ENV=development

To start the server set the package name 'hub' and run Flask in the hub folder:

    (.venv) C:\GIT\Repositories\Social-Media-Text-Annotator>set FLASK_APP=hub


## Initialize and populate database

Flask populate-db command creates database models, and populates User, TextContent, and TextAnnotation models.
Init flask database basedir hub:

    (.venv) C:\Social-Media-Text-Annotator>flask init-db

Populate flask database:

    (.venv) C:\Social-Media-Text-Annotator\HateSpeechAnnotator>flask populate-db

API downloads excel file defined at "models.py" -file from "data" -folder.


## Run flask API

Run flask local host at http://localhost:5000/admin/ with command:

    (.venv) C:\Social-Media-Text-Annotator\HateSpeechAnnotator>flask run

Open Social-Media-Text-Annotator API at local host window by command:

    http://localhost:5000/admin/


## Quit the use of flask API

Quit the use of API with following command in cmd:

    CTRL+C


## Deactivate venv

Deactivate virtual environment with following command in cmd:

    deactivate


## Relocate and delete database

Relocate and delete created database (for example 'developmentHateSpeech.db') before initiation of new database file.
