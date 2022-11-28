# Meria's Annotator for Social Media Texts
# University of Oulu
# Created by Merja Kreivi-Kauppinen (2021-2022)

# Social-Media-Text-Annotator/HateSpeechAnnotator API database models - models.py
# This file includes database models of HateSpeechAnnotator API.

# check / change launch.json -file parameters and location if debugging with VSC or Postman

# -------------------------------------------------------------------------------------------

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

# database model for text content ------------------------------------------------------------

class TextContent(db.Model):
    __tablename__ = 'textcontent'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"))

    sample = db.Column(db.String(1024), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    text_annotations = db.relationship("TextAnnotation", back_populates="texts")
    text_users = db.relationship("User", back_populates="text_user", uselist=True)

# database model for text annotation ---------------------------------------------------------

class TextAnnotation(db.Model):
    __tablename__ = 'textannotation'
    id = db.Column(db.Integer, primary_key=True)
    text_id = db.Column(db.Integer, db.ForeignKey("textcontent.id", ondelete="SET NULL"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"))
    HS_binary = db.Column(db.Boolean, nullable=False)
    HS_strength= db.Column(db.Integer, nullable=False)
    HS_target = db.Column(db.String(128), nullable=True)
    HS_topic = db.Column(db.String(128), nullable=True)
    HS_form = db.Column(db.String(128), nullable=True)
    sentiment = db.Column(db.String(128), nullable=True)
    polarity = db.Column(db.Integer, nullable=True)
    main_emotion = db.Column(db.String(128), nullable=True)
    urban_finnish = db.Column(db.String(1024), nullable=True)
    correct_finnish = db.Column(db.String(1024), nullable=True)

    texts = db.relationship("TextContent", back_populates="text_annotations", uselist=True)
    text_annotators = db.relationship("User", back_populates="text_annotator", uselist=True)

# database model for user -------------------------------------------------------------------
# user name is unique - password is not necessary - CHECK CLIENT !!!!!
# nick name is unique

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
# create database and popuate it for test and development purposes

@click.command("init-db")
@with_appcontext

def init_db_command():
    db.create_all()

@click.command("populate-db")
@with_appcontext

def generate_test_data():

    #(upload_text_folder) = create_static_folders()
    # Create row for new user to database by using User -model
    user1 = User(user_name = "Meria Developer", user_password="mötkäle", user_nick="Meria")
    user2 = User(user_name = "Vili Visitor", user_password="kukka", user_nick = "Visitor",)
    user3 = User(user_name = "Test Engineer", user_password="1234test", user_nick = "Tester",)
    
    # Add model to the session
    db.session.add_all([user1])
    db.session.add_all([user2])
    db.session.add_all([user3])
    
    # Add model to the session
    # db.session.add_all([user1, user2, user3])
    
    # Save session to database with commit
    db.session.commit()

    print("\nADD USER \n")

    # Execute SQL query for database by using Model.query
    # OR for db.session.query(Model)
    # query.all() get all rows in the database as a list
    result_users = User.query.all()
    for item in result_users:
        print("User object: ", item ,"   User ID: ", item.id, "   Username:  ", item.user_name, "   User nick:  ", item.user_nick, "   User password:  ", item.user_password)
        
    # Collect defined user from database
    userqueried = User.query.filter_by(user_name="Meria Developer").first()

    # Add text samples of sample_list (collected from defined folder in path) for defined user in database
    # and commit to database
    textRows = getCSVData()
    dictionaryList = textRows.to_dict('index')
    print(dictionaryList)

    i = 0
    while i < len(dictionaryList):
        
        textObj = TextContent(sample=dictionaryList[i]["sample"])
        userqueried.text_user.append(textObj)
        db.session.commit()

        annotationObj = TextAnnotation(HS_binary=dictionaryList[i]["HSbinary"], 
                                        HS_strength=dictionaryList[i]["HSstrength"],
                                        HS_target=dictionaryList[i]["HStarget"],
                                        HS_topic=dictionaryList[i]["HStopic"],
                                        HS_form=dictionaryList[i]["HSform"],
                                        sentiment=dictionaryList[i]["sentiment"],
                                        polarity=dictionaryList[i]["polarity"],
                                        main_emotion=dictionaryList[i]["mainEmotion"],
                                        urban_finnish=dictionaryList[i]["urbanFinnish"],
                                        correct_finnish=dictionaryList[i]["correctFinnish"])
        userqueried.text_annotator.append(annotationObj)
        textObj.text_annotations.append(annotationObj)
        #textObj = TextContent(sample=dictionaryList[i]["sample"], text_annotations=annotationObj)
                        
        db.session.commit()
        i= i+1
    
# -------------------------------------------------------------------------------

def getCSVData():
    cwd = os.getcwd()
    folder = '\\data\\'
    csv_file = 'HS_ALL_TEST_SET.xlsx'
    csv_source = cwd + folder + csv_file
    return pd.read_excel(csv_source, nrows=100)
