# Meria's Social Media Text Annotator

Meria's Annotator for social media text samples was created as a part of scientific work of thesis. 
It was created by Merja Kreivi-Kauppinen (2021-2022) at University of Oulu.
Meria's Annotator facilitates manual hate speech labeling process.

![mountain_of_worries](https://user-images.githubusercontent.com/55892486/203412060-c6f75570-cea6-4150-9c05-f314dacc7f1a.png)

Meria's Annotator includes small GUI for the Social-Media-Text-Annotator API. 
This web API is programmed with Python, Flask RESTful, Flask SQLAlchemy, SQLite, jQuery, Vanilla JavaScript, HTML and CSS Bootstrap. 

With help of the Social-Media-Text-Annotator API client you can import social media text samples into database, manually label saved text samples, and keep all samples and annotations available in the database. 
API and database create an environment for multiple users.

## Getting started

It is recommended to use virtual environment for using and testing the code. Usage of Python 3.7 or newer version is required. 
Use "pip install" to install virtual environment packages. The code package of Social Media Text Annotator API needs for example following python library packages:

    Flask, pysqlite3, Flask-sqlalchemy, flask-restful, pytest, pytest-cov, Flask-Script, Flask-Migrate, Pillow, jsonschema, requests, pandas

## Set up python virtual environment for flask project

Open command prompt (cmd) and proceed to C root folder. Clone Social-Media-Text-Annotator project using following command. The command will create folder C:\Social-Media-Text-Annotator.

    C:\>git clone https://github.com/MerjaKreivi/Social-Media-Text-Annotator.git

Create virtual environment on Social-Media-Text-Annotator folder.

    C:\Social-Media-Text-Annotator\python -m venv .venv

Next activate created python virtual environment (on cmd):

    C:\Social-Media-Text-Annotator\.venv\Scripts>activate.bat

## Install required python libraries

Install packages defined at "requirements.txt" -file with  following command in cmd:

    (.venv) C:\Social-Media-Text-Annotator>pip install -r requirements.txt

Install project with pip in editable (-e) mode with dot (.)

    (.venv) C:\Social-Media-Text-Annotator>pip install -e .

## Set up configuration for flask

In order run Meria's Annotator flask API set up virtual environment, 
activate virtual environment, set flask, init database and populate database.

Set cofiguration setting class as 'development' or 'production' or 'default' or 'testing'

    (.venv) C:\GIT\Repositories\Social-Media-Text-Annotator>set FLASK_ENV=development

To start the server set the package name 'hub' and run Flask in the hub folder:

    (.venv) C:\GIT\Repositories\Social-Media-Text-Annotator>set FLASK_APP=hub

## Initialize and populate database

Flask populate-db command creates database models, and populates User, TextContent, and TextAnnotation models.
Init flask database basedir hub:

    (.venv) C:\Social-Media-Text-Annotator>flask init-db

Populate flask database:

    (.venv) C:\Social-Media-Text-Annotator\HateSpeechAnnotator>flask populate-db

API downloads excel file defined at "test_read_csv_to_dict.py" -file.

## Run flask API

Run flask local host at http://localhost:5000/admin/ with command:

    (.venv) C:\Social-Media-Text-Annotator\HateSpeechAnnotator>flask run

Open Social-Media-Text-Annotator API at local host window by command:

    http://localhost:5000/admin/
