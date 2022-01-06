# PWP course 2021 University of Oulu
# created by Merja Kreivi-Kauppinen

# Image Annotator API database models - models.py
# This file includes database models of Image Annotator API.

# check / change launch.json -file parameters and location if debugging with VSC or Postman

# --------------------------------------------------------------------------------------------

# The first time the app runs it creates the table. 
# BE CAREFULL - With this code you can override the default table name

# cd C:\PWPproject\ImageAnnotator\.venv\Scripts
# activate.bat
# C:\PWPproject\ImageAnnotator>
# set FLASK_ENV=development (or testing)
# set FLASK_APP=hub
# flask init-db
# flask populate-db
# flask run

# --------------------------------------------------------------------------------------------
"""
In order run ImageAnnotator flask API and this file 
activate virtual environment, set flask, init database and populate database.

Activate created python virtual environment (on cmd):
    cd C:\PWPproject\ImageAnnotator\.venv\Scripts
    activate.bat

Go to ImageAnnotator folder: (provide 'cd ..' on cmd)
    (.venv) C:\PWPproject\ImageAnnotator>

Set cofiguration setting class as 'development' or 'production' or 'default' or 'testing'
    (.venv) C:\PWPproject\ImageAnnotator>set FLASK_ENV=development

In order to start the server set the package name 'hub' and run Flask in the hub folder:
    (.venv) C:\PWPproject\ImageAnnotator>set FLASK_APP=hub

Init flask database basedir hub:
    (.venv) C:\PWPproject\ImageAnnotator>flask init-db

Populate flask database:
    (.venv) C:\PWPproject\ImageAnnotator>flask populate-db

Run flask local host at http://localhost:5000/admin/

    (.venv) C:\PWPproject\ImageAnnotator>flask run

This code creates database models, 
and populates User, PhotoContent, PhotoAnnotation, ImageContent and ImageAnnotation models
"""
# --------------------------------------------------------------------------------------------

import os
import sys
import glob
from io import BytesIO
import pandas as pd

from datetime import datetime
from typing import Text
import click
from flask.cli import with_appcontext

from shutil import copy

from hub import db
from hub.constants import *

# database model for image content and photo content -----------------------------------------

class TextContent(db.Model):
    __tablename__ = 'textcontent'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"))

    HSOriginalComment = db.Column(db.String(1024), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    text_annotations = db.relationship("TextAnnotation", back_populates="texts")
    text_users = db.relationship("User", back_populates="text_user", uselist=True)

# database model for imageannotation ---------------------------------------------------------

class TextAnnotation(db.Model):
    __tablename__ = 'textannotation'
    id = db.Column(db.Integer, primary_key=True)
    text_id = db.Column(db.Integer, db.ForeignKey("textcontent.id", ondelete="SET NULL"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"))
    HS_binary = db.Column(db.Boolean, nullable=False)
    HS_class= db.Column(db.Integer, nullable=False)
    HS_category = db.Column(db.String(128), nullable=True)
    SentencePolarity = db.Column(db.Integer, nullable=True)
    SentenceEmotionCategory = db.Column(db.String(128), nullable=True)
    HSinUrbanFinnish = db.Column(db.String(1024), nullable=True)
    HSinFinnish = db.Column(db.String(1024), nullable=True)

    texts = db.relationship("TextContent", back_populates="text_annotations", uselist=True)
    text_annotators = db.relationship("User", back_populates="text_annotator", uselist=True)


# database model for user -------------------------------------------------------------------
# user name is unique - password is not necessary - CHECK CLIENT !!!!!

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(128), unique=True, nullable=False)
    user_password = db.Column(db.String(32), nullable=True)
    user_nick = db.Column(db.String(128), unique=True, nullable=False)

    text_user = db.relationship("TextContent", back_populates="text_users")    

    text_annotator = db.relationship("TextAnnotation", back_populates="text_annotators")    


# --------------------------------------------------------------------------------------------
# HELPER FUNCTIONS - CLICK COMMANDS
# create database and popuate it for test and dvelopment purposes

@click.command("init-db")
@with_appcontext

def init_db_command():
    db.create_all()

@click.command("populate-db")
@with_appcontext


def generate_test_data():

    #(upload_images_folder, upload_photos_folder) = create_static_folders()

    # Create row for new user to database by using User -model
    user1 = User(user_name = "Meria Developer", user_password="mötkäle", user_nick="Merja")
    
    # Add model to the session
    db.session.add_all([user1])
    # Save session to database with commit
    db.session.commit()

    # Collect defined user from database
    userqueried = User.query.filter_by(user_name="Meria Developer").first()

    # Add images of image_list (collected from defined folder in path) for defined user in database
    # and commit to database
    textRows = getCSVData()
    dictionaryList = textRows.to_dict('index')

    i = 0
    while i < len(dictionaryList):
        
        textObj = TextContent(HSOriginalComment=dictionaryList[i]["HSoriginalComment"])
        userqueried.text_user.append(textObj)
        db.session.commit()

        annotationObj = TextAnnotation(HS_binary=dictionaryList[i]["HSbinary"], 
                                        HS_class=dictionaryList[i]["HSclass"],
                                        HS_category=dictionaryList[i]["HScategory"],
                                        SentencePolarity=dictionaryList[i]["sentencePolarity"],
                                        SentenceEmotionCategory=dictionaryList[i]["sentenceEmotionCategory"],
                                        HSinUrbanFinnish=dictionaryList[i]["HSinUrbanFinnish"],
                                        HSinFinnish=dictionaryList[i]["HSinFinnish"])
        userqueried.text_annotator.append(annotationObj)
        textObj.text_annotations.append(annotationObj)
        #textObj = TextContent(HSOriginalComment=dictionaryList[i]["HSoriginalComment"], text_annotations=annotationObj)
                        
        db.session.commit()
        i= i+1
    
# -------------------------------------------------------------------------------

def getCSVData():
    cwd = os.getcwd()
    folder = '\\data\\'
    csv_file = 'HS_ALL_TEST_SET.xlsx'
    csv_source = cwd + folder + csv_file
    return pd.read_excel(csv_source, nrows=10)
