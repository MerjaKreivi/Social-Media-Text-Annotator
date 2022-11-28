# Meria's Annotator for Social Media Texts
# University of Oulu
# Created by Merja Kreivi-Kauppinen (2021-2022)

# Social-Media-Text-Annotator/HateSpeechAnnotator API utils.py
# This file defines Mason builder classes

# ------------------------------------------------------------------------

import json
import base64
import glob
from io import BytesIO
from datetime import datetime
from flask import Response, request, url_for

#import hub.api_routes
from hub.constants import *
#import hub.models
from hub.models import *

# define Mason Builder Class ------------------------------------------------------

class MasonBuilder(dict):
    """
    A convenience class for managing dictionaries that represent Mason
    objects. It provides nice shorthands for inserting some of the more
    elements into the object but mostly is just a parent for the much more
    useful subclass defined next. This class is generic in the sense that it
    does not contain any application specific implementation details.
    """

    def add_error(self, title, details):
        """
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.
        Note: Mason allows more than one string in the @messages property (it's
        in fact an array). 
        However we are being lazy and supporting just one message.
        : param str title: Short title for the error
        : param str details: Longer human-readable description
        """

        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, ns, uri):
        """
        Adds a namespace element to the object. 
        A namespace defines where our link relations are coming from. 
        The URI can be an address where
        developers can find information about our link relations.
        : param str ns: the namespace prefix
        : param str uri: the identifier URI of the namespace
        """

        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][ns] = {
            "name": uri
        }

    def add_control(self, ctrl_name, href, **kwargs):
        """
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. 
        Technically only certain properties are allowed for kwargs 
        but we're being lazy and don't perform any checking.
        The allowed properties can be found from here
        https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md
        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        """

        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs
        self["@controls"][ctrl_name]["href"] = href
    
    def add_pagecount(self, pagecount):
        self["@pagecount"] = pagecount

    def add_info_string(self, info_string):
        self["@infostring"] = info_string


# -------------------------------------------------------------------------------------------------
# Define hub builder class and create hub builder with MasonBuilder

class HubBuilder(MasonBuilder):

    ##### user --------------------------------------------------

    @staticmethod
    def user_schema():
        schema = {
            "type": "object",
            "required": ["user_name", "user_password"]
        }
        props = schema["properties"] = {}
        props ["user_name"] = {
            "description": "Name of the user",
            "type": "string"
        }
        props ["user_password"] = {
            "description": "Password of the user",
            "type": "string"
        }
        return schema

    def add_control_add_user(self):
        """
        Control to add user
        """
        self.add_control(
            "annometa:add-user",
            url_for("api.usercollection"),
            method="POST",
            encoding="json",
            title="Add new user",
            schema=self.user_schema()
        )
    
    def add_control_delete_user(self, user_name):
        """
        Control to delete user
        """
        self.add_control(
            "annometa:delete",
            url_for("api.useritem", user_name=user_name),
            method="DELETE",
            title="Delete user"
        )

    def add_control_edit_user(self, user_name):
        """
        Control to edit user
        """
        self.add_control(
            "edit",
            url_for("api.useritem", user_name=user_name),
            method="PUT",
            encoding="json",
            title="Edit user",
            schema=self.user_schema()
        )

    ##### login -----------------------------------------------------
    
    def add_control_login_user(self):
        """
        Control to login user
        """
        self.add_control(
            "annometa:login",
            url_for("api.userlogin"),
            method="POST",
            encoding="json",
            title="Login user",
            schema=self.user_schema()
        )

    ##### text -----------------------------------------------------

    @staticmethod
    def text_schema():
        schema = {
            "type": "object",
            "required": ["sample"]
        }
        props = schema["properties"] = {}
        props ["sample"] = {
            "description": "Social media text sample in string form",
            "type": "string"
        }        
        #props ["date"] = {
        #    "description": "Text upload timestamp",
        #    "type": "string",
        #    "pattern": "^[0-9]{4}-[01][0-9]-[0-3][0-9]T[0-9]{2}:[0-5][0-9]:[0-5][0-9]Z$"
        #}
        return schema
    
    def add_control_add_text(self):
        self.add_control(
            "annometa:add-text",
            url_for("api.textcollection"),
            method="POST",
            encoding="json",
            title="Add a new text to text collection",
            schema=self.text_schema()
        )

    def add_control_delete_text(self, id):
        self.add_control(
            "annometa:delete",
            url_for("api.textitem", id=id),
            method="DELETE",
            title="Delete this text"
        )
    
    def add_control_edit_text(self, id):
        self.add_control(
            "annometa:edit",
            url_for("api.textitem", id=id),
            method="PUT",
            encoding="json",
            title="Edit this text",
            schema=self.text_schema()
        )    

    def add_control_get_text(self, id):
        self.add_control(
            "annometa:text",
            "/api/texts/text/",
            url_for("api.textitem", id=id),
            method="GET",
            encoding="json",
            title="Add control to get text",
            schema=self.text_schema()
            )

    def add_control_all_texts(self):
        self.add_control(
            "annometa:texts",
            "/api/texts/",
            method="GET",
            encoding="json",
            title="Add control to get all texts",
            schema=self.text_schema()
            )

#### textannotation -----------------------------------------------------

    @staticmethod
    def textannotation_schema():
        schema = {
            "type": "object",
            "required": ["HS_binary", "HS_strength",
            "HS_target","HS_topic","HS_form",
            "sentiment", "polarity", "main_emotion",
            "urban_finnish", "correct_finnish"]
        }
        props = schema["properties"] = {}
        props ["HS_binary"] = {
            "description": "Category to define if text is hate speech",
            "type": "boolean"
        }
        props ["HS_strength"] = {
            "description": "Category to define how hateful hate speech is",
            "type": "number"
        }       
        props ["HS_target"] = {
            "description": "Category to define target subcategory for hate speech",
            "type": "string"
        }
        props ["HS_topic"] = {
            "description": "Category to define topic subcategory for hate speech",
            "type": "string"
        }
        props ["HS_form"] = {
            "description": "Category to define form subcategory for hate speech",
            "type": "string"
        }
        props ["sentiment"] = {
            "description": "Category to define sentiment subcategory for text sample",
            "type": "string"
        }
        props ["polarity"] = {
            "description": "Category to define polarity value for text sample",
            "type": "number"
        }
        props ["main_emotion"] = {
            "description": "Category to define main emotion subcategory for text sample",
            "type": "string"
        }
        props ["urban_finnish"] = {
            "description": "Text sample in urban Finnish - separated words",
            "type": "string"
        }
        props ["correct_finnish"] = {
            "description": "Text sample in literal and correct Finnish",
            "type": "string"
        }
        return schema

    def add_control_add_textannotation(self):
        self.add_control(
            "annometa:add-textannotation",
            url_for("api.textannotationcollection"),
            method="POST",
            encoding="json",
            title="Add new annotation to text annotation collection",
            schema=self.textannotation_schema()
        )

    def add_control_delete_textannotation(self, id):
        self.add_control(
            "annometa:delete",
            url_for("api.textannotationitem", id=id),
            method="DELETE",
            title="Delete text annotation"
        )

    def add_control_edit_textannotation(self, id):
        self.add_control(
            "edit",
            url_for("api.textannotationitem", id=id),
            method="PUT",
            encoding="json",
            title="Edit text annotation",
            schema=self.textannotation_schema()
        )

    def add_control_get_textannotation(self, id):
        self.add_control(
            "annometa:textannotation",
            "/api/textannotations/textannotation/",
            url_for("api.textannotationitem", id=id),
            method="GET",
            encoding="json",
            title="Add control to get this text annotation",
            schema=self.textannotation_schema()
            )

    def add_control_all_textannotations(self):
        self.add_control(
            "annometa:textannotations",
            "/api/textannotations/",
            method="GET",
            encoding="json",
            title="Add control to get all text annotations",
            schema=self.textannotation_schema()
            )

### Data collection by nickname

    def add_control_all_database(self):
        self.add_control(
            "annometa:datacollectionbynickname",
            "/api/datacollectionbynickname/",
            method="GET",
            encoding="json",
            title="Add control to get all data by nickname",
            schema=self.textannotation_schema()
            )

# Define error response function ---------------------------------------------------

def create_error_response(status_code, title, message=None):
    resource_url = request.path
    body = MasonBuilder(resource_url=resource_url)
    body.add_error(title, message)
    body.add_control("profile", href=ERROR_PROFILE)
    return Response(json.dumps(body), status_code, mimetype=MASON)

# ----------------------------------------------------------------------------------
