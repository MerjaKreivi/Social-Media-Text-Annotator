# Meria's Annotator for Social Media Texts
# University of Oulu
# Created by Merja Kreivi-Kauppinen (2021-2022)

# Social-Media-Text-Annotator/HateSpeechAnnotator API resources.py
# This file includes resources of HateSpeechAnnotator API

# ---------------------------------------------------------------------------------------

import os
import sys
import math
from io import BufferedReader

import json
from jsonschema import validate, ValidationError
from datetime import datetime
from pathlib import Path, PurePath

from flask import Response, request, url_for, abort
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine


#from hub import db or database
#import hub.api_routes
#from hub.api_routes import *

from hub.constants import *
import hub.models
from hub.models import *
import hub.utils
from hub.utils import *

# -----------------------------------------------------------------------------------------
# defined in constants file
# UPLOAD_FOLDER = "\\static\\images\\"
# ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'gif', 'bmp', 'tiff'])

# -----------------------------------------------------------------------------------------
# helper functions

# convert datetime to string
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


# ------------------------------------------------------------------------------------------
# User and UserCollection Resources

class UserCollection(Resource):
    """
    Resource for UserCollection. 
    Function GET gets all the users in collection
    and function POST adds a new user to collection.
    """

    def get(self):
        """
        GET method gets all the users from collection
        """
        body = HubBuilder()
        body.add_namespace("annometa", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.usercollection"))
        body.add_control_add_user()
        body["items"] = []

        for db_user in User.query.all():
            item = HubBuilder(
                user_name=db_user.user_name,
                user_password=db_user.user_password
            )
            # item.add_control("self", url_for("api.usercollection")) # merja
            item.add_control("self", url_for("api.useritem", user_name=db_user.user_name))
            item.add_control("profile", USER_PROFILE)
            body["items"].append(item)
        body.add_control_login_user()
        return Response(json.dumps(body), status=200, mimetype=MASON)


    def post(self):
        """
        POST method adds a new user to collection
        """
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            # validate(request.json, User.user_schema())
            validate(request.json, HubBuilder.user_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        new_user = User(
            user_name=request.json["user_name"],
            user_password=request.json["user_password"]
        )
        try:
            db.session.add(new_user)
            db.session.commit()

        except IntegrityError:
            return create_error_response(409, "Username already exists", "User with name '{}' already exists in database. Choose new username.".format(request.json["user_name"]))

        # tarkista alla oleva rivi !!!
        return Response(status=201, headers={"Location": url_for("api.useritem", user_name=request.json["user_name"])})


class UserLogin(Resource):
    """
    New resource !!! POST for login purposes
    """
    def post(self):
        """
        POST method for user login
        """
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            # validate(request.json, User.user_schema())
            validate(request.json, HubBuilder.user_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))
        
        user_name=request.json["user_name"]
        user_password=request.json["user_password"]

        db_user = User.query.filter_by(user_name=user_name).first()
        
        if db_user is None:
            return create_error_response(404, "Not found", "No user was found with name {}".format(user_name))

        if (db_user.user_password == user_password):
            return Response(status=200, headers={"Location": url_for("api.useritem", user_name=user_name)})
        else:
            return create_error_response(401, "Invalid password", "Invalid password for {}".format(user_name))


class UserItem(Resource):
    """
    Resource for single UserItem. 
    Function GET gets a user, PUT edits a user and DELETE deletes a user.
    """    
        
    def get(self, user_name):
        """
        GET method gets a single user
        """
        db_user = User.query.filter_by(user_name=user_name).first()
        if db_user is None:
            return create_error_response(404, "Not found", "No user was found with name {}".format(user_name))

        body = HubBuilder(
            user_name=db_user.user_name,
            user_password=db_user.user_password
        )

        body.add_namespace("annometa", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.useritem", user_name=user_name))
        body.add_control("profile", USER_PROFILE)
        body.add_control("collection", url_for("api.usercollection"))
        body.add_control_delete_user(user_name)
        body.add_control_edit_user(user_name)

        return Response(json.dumps(body), status=200, mimetype=MASON)

    def put(self, user_name):
        """
        PUT method edits user_password (and/or other user specific data)
        """
        db_user = User.query.filter_by(user_name=user_name).first()
        
        if db_user is None:
            return create_error_response(404, "Not found", "No user was found with name {}".format(user_name))
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, HubBuilder.user_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))
                
        db_user.user_password = request.json["user_password"]
        db.session.commit()
        return Response(status=204)

    def delete(self, user_name):
        """
        DELETE method deletes a user
        """
        db_user = User.query.filter_by(user_name=user_name).first()
        if db_user is None:
            return create_error_response(404, "Not found", "No user was found with name {}".format(user_name))

        db.session.delete(db_user)
        db.session.commit()

        return Response(status=204)


class TextItem(Resource):
    """
    Resource for TextItem. 
    Function GET gets one single text, PUT edits the text, and DELETE deletes the text.
    """

    def get(self, id):
        """
        GET method gets one single text
        """
        db_text = TextContent.query.filter_by(id=id).first()
        if db_text is None:
            return create_error_response(404, "Not found", "No text was found with id {}".format(id))        

        body = HubBuilder(
                id = db_text.id,
                user_id = db_text.user_id,
                HSOriginalComment = db_text.HSOriginalComment,
                date = db_text.date
        )

        body.add_namespace("annometa", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.textitem", id=id))
        body.add_control("profile", TEXT_PROFILE)
        body.add_control("collection", url_for("api.textcollection"))
        if db_text.text_annotations != []:            
            body.add_control("textannotation", url_for("api.textannotationitem", id=db_text.text_annotations[0].id))
        else:
            body.add_control("textannotations", url_for("api.textannotationcollection"))
        body.add_control_delete_text(id)
        body.add_control_edit_text(id)

        # definition default=str below because of datetime objects
        return Response(json.dumps(body, default=str), status=200, mimetype=MASON)

    def put(self, id):
        """
        PUT method edits one single text 
        """
        db_text = TextContent.query.filter_by(id=id).first()

        if db_text is None:
            return create_error_response(404, "Not found", "No text was found with id {}".format(id))
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")

        if "HSModifiedComment" in request.json:
            if request.json["HSModifiedComment"] == "" or request.json["HSModifiedComment"] == None:
                return create_error_response(400, "Invalid JSON document", "No edited text provided")
        else:
            return create_error_response(400, "Invalid JSON document", "No file name provided")      
        
        db_text.HSOriginalComment = request.json["HSModifiedComment"]
        db.session.commit()        
        
        return Response(status=204, headers={"Location": url_for("api.textitem", id=db_text.id)})

    def delete(self, id):
        """
        DELETE method deletes one single text
        """
        db_text = TextContent.query.filter_by(id=id).first()
        if db_text is None:
            return create_error_response(404, "Not found", "No text was found with id {}".format(id))
        
        db.session.delete(db_text)
        db.session.commit()
        return Response(status=204)

class TextCollection(Resource):
    """
    Resource for TextCollection. 
    Function GET gets all the texts in collection and POST adds a new text to collection.
    """

    def get(self):
        """
        GET method gets all the texts from TextCollection
        """
        body = HubBuilder()
        body.add_namespace("annometa", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.textcollection"))
        body.add_control_add_text()
        body["items"] = []                
        
        for text in TextContent.query.all():
        
            item = HubBuilder(
                id = text.id,
                user_id = text.user_id,
                HSOriginalComment = text.HSOriginalComment,
                date = text.date
            )
            item.add_control("self", url_for("api.textitem", id=text.id))
            item.add_control("profile", TEXT_PROFILE)
            if text.text_annotations != []:
                item.add_control("textannotation", url_for("api.textannotationitem", id=text.text_annotations[0].id))
            body["items"].append(item)
        
        # definition default=str below because of datetime objects
        return Response(json.dumps(body, default=str), status=200, mimetype=MASON)
    
    def post(self):
        """
        POST method adds a new text to TextCollection
        """       
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, HubBuilder.text_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))
                
        if "user_name" in request.json:
            if request.json["user_name"] == "" or request.json["user_name"] == None:
                return create_error_response(400, "Invalid JSON document", "No user name provided")
        else:
            return create_error_response(400, "Invalid JSON document", "No user name provided")

        # query current user from database
        currentUser = User.query.filter_by(user_name=request.json["user_name"]).first() 

        new_text = TextContent(            
            user_id = request.json["user_name"],
            HSOriginalComment = request.json["HSOriginalComment"]            
        )

        try:
            currentUser.text_user.append(new_text)
            db.session.commit()
            
             # query the newly added annotation             
            db_text = TextContent.query.filter_by(id=new_text.id).first()
            return Response(status=201, headers={"Location": url_for("api.textitem", id=db_text.id)})
            
        except IntegrityError:
            return create_error_response(409, "Already exists", "Text with id '{}' already exists".format(request.json["id"]))

class TextItemCount(Resource):
    def get(self):
        body = HubBuilder(
            numberOfItems = TextContent.query.count()                
        )        
        body.add_control("self", url_for("api.textcollection"))                

        # definition default=str below because of datetime objects
        return Response(json.dumps(body, default=str), status=200, mimetype=MASON)        

class TextItemPageCount(Resource):
    def get(self, itemsOnPage):
        pages = 1
        numberOfItems = TextContent.query.count()
        if (numberOfItems > 0):
            try:
                asInt = int(itemsOnPage)
                if asInt > 0:
                    if (numberOfItems > asInt):
                        pages = math.ceil(numberOfItems/asInt)                
                body = HubBuilder(
                        numberOfPages = pages
                )
                # definition default=str below because of datetime objects
                return Response(json.dumps(body, default=str), status=200, mimetype=MASON)        
            except IntegrityError:
                return create_error_response(415, "Unsupported media type", "Item count must be an integer as string.")
            
class TextAnnotationCollection(Resource):
    """
    Resource for TextAnnotationCollection. 
    Function GET gets all the text annotations in collection
    and POST adds a new text annotation to collection.
    """

    def get(self):
        """
        GET method gets all text annotations from TextAnnotationCollection
        """
        body = HubBuilder()
        body.add_namespace("annometa", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.textannotationcollection"))
        body.add_control_add_textannotation()
        body["items"] = []

        for db_text in TextAnnotation.query.all():

            item = HubBuilder(
                id = db_text.id,
                text_id = db_text.text_id,
                user_id = db_text.user_id,
                HS_binary = db_text.HS_binary,
                HS_class = db_text.HS_class,
                HS_category = db_text.HS_category,
                SentencePolarity = db_text.SentencePolarity,
                SentenceEmotionCategory = db_text.SentenceEmotionCategory,
                HSinUrbanFinnish = db_text.HSinUrbanFinnish,
                HSinFinnish = db_text.HSinFinnish
            )
            item.add_control("self", url_for("api.textannotationcollection"))
            item.add_control("profile", TEXTANNOTATION_PROFILE)
            body["items"].append(item)
        return Response(json.dumps(body), status=200, mimetype=MASON)

    def post(self):
        """
        POST method adds a new text to TextCollection
        """       
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")
        try:
            validate(request.json, HubBuilder.textannotation_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))
        
        if "text_id" in request.json:
            if request.json["text_id"] == "" or request.json["text_id"] == None:
                return create_error_response(400, "Invalid JSON document", "No text id provided")
        else:
            return create_error_response(400, "Invalid JSON document", "No text id provided")   
       
        if "user_id" in request.json:
            if request.json["user_id"] == "" or request.json["user_id"] == None:
                return create_error_response(400, "Invalid JSON document", "No user id provided")
        else:
            return create_error_response(400, "Invalid JSON document", "No user id provided")

        new_textannotation = TextAnnotation(
            text_id = request.json["text_id"],
            user_id = request.json["user_id"],
            HS_binary = request.json["HS_binary"],
            HS_class = request.json["HS_class"],
            HS_category = request.json["HS_category"],
            SentencePolarity = request.json["SentencePolarity"],
            SentenceEmotionCategory = request.json["SentenceEmotionCategory"],
            HSinUrbanFinnish = request.json["HSinUrbanFinnish"],
            HSinFinnish = request.json["HSinFinnish"],            
        )

        try:
            db.session.add(new_textannotation)
            db.session.commit()

             # query the newly added annotation             
            db_annotation = TextAnnotation.query.filter_by(text_id=new_textannotation.text_id).first()
            return Response(status=201, headers={"Location": url_for("api.textannotationitem", id=db_annotation.id)})
            
        except IntegrityError:
            return create_error_response(409, "Already exists", "Text annotation with id '{}' already exists".format(request.json["id"]))

class TextAnnotationItem(Resource):
    """
    Resource for TextAnnotationItem. 
    Function GET gets one single text annotation, PUT edits a text annotation,
    and DELETE deletes a text annotation.
    """

    def get(self, id):
        """
        GET method gets one single text annotation
        """
        db_text = TextAnnotation.query.filter_by(id=id).first()
        if db_text is None:
            return create_error_response(404, "Not found", "No text annotation was found with id {}".format(id))

        # query annotator for annotator control
        annotator = User.query.filter_by(id=db_text.user_id).first()

        body = HubBuilder(
            id = db_text.id,
            text_id = db_text.text_id,
            user_id = db_text.user_id,
            HS_binary = db_text.HS_binary,
            HS_class = db_text.HS_class,
            HS_category = db_text.HS_category,
            SentencePolarity = db_text.SentencePolarity,
            SentenceEmotionCategory = db_text.SentenceEmotionCategory,
            HSinUrbanFinnish = db_text.HSinUrbanFinnish,
            HSinFinnish = db_text.HSinFinnish
        )

        body.add_namespace("annometa", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.textannotationitem", id=id))
        body.add_control("profile", TEXTANNOTATION_PROFILE)
        body.add_control("collection", url_for("api.textannotationcollection"))
        body.add_control("textitem", url_for("api.textitem", id=db_text.text_id))
        body.add_control("annotator", url_for("api.useritem", user_name=annotator.user_name))
        body.add_control_delete_textannotation(id)
        body.add_control_edit_textannotation(id)

        return Response(json.dumps(body), status=200, mimetype=MASON)


    def put(self, id):
        """
        PUT method edits one single text annotation
        """
        db_text_anno = TextAnnotation.query.filter_by(id=id).first()

        if db_text_anno is None:
            return create_error_response(404, "Not found", "No text annotation was found with id {}".format(id))
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")

        if "text_id" in request.json:
            if request.json["text_id"] == "" or request.json["text_id"] == None:
                return create_error_response(400, "Invalid JSON document", "No text id provided")
        else:
            return create_error_response(400, "Invalid JSON document", "No text id provided")   

        if "user_id" in request.json:
            if request.json["user_id"] == "" or request.json["user_id"] == None:
                return create_error_response(400, "Invalid JSON document", "No user id provided")
        else:
            return create_error_response(400, "Invalid JSON document", "No user id provided")   

        try:
            validate(request.json, HubBuilder.textannotation_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        db_text_anno.user_id=request.json["user_id"]
        db_text_anno.HS_binary = request.json["HS_binary"]
        db_text_anno.HS_class = request.json["HS_class"]
        db_text_anno.HS_category = request.json["HS_category"]
        db_text_anno.SentencePolarity = request.json["SentencePolarity"]
        db_text_anno.SentenceEmotionCategory = request.json["SentenceEmotionCategory"]
        db_text_anno.HSinUrbanFinnish = request.json["HSinUrbanFinnish"]
        db_text_anno.HSinFinnish = request.json["HSinFinnish"]        

        try:
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists", "Text annotation with id '{}' already exists".format(request.json["id"]))
        return Response(status=204, headers={"Location": url_for("api.textannotationitem", id=db_text_anno.id)})


    def delete(self, id):
        """
        DELETE method deletes one single text annotation
        """
        db_textanno = TextAnnotation.query.filter_by(id=id).first()
        if db_textanno is None:
            return create_error_response(404, "Not found", "No text annotation was found with id {}".format(id))

        db.session.delete(db_textanno)
        db.session.commit()
        return Response(status=204)
