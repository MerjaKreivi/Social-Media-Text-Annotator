# Meria's Annotator for Social Media Texts
# University of Oulu
# Created by Merja Kreivi-Kauppinen (2021-2022)

# Social-Media-Text-Annotator/HateSpeechAnnotator API api_routes.py
# This file defines and ads recources to api
# ------------------------------------------------------------------------

from flask import Blueprint
from flask_restful import Api

# import hub.resources
from hub.resources import UserItem, UserCollection, UserLogin
from hub.resources import TextItem, TextCollection, TextItemCount, TextItemPageCount, TextItemsInPages
from hub.resources import TextAnnotationItem, TextAnnotationCollection

# -----------------------------------------------------------
# define api blueprint prefix

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

# -----------------------------------------------------------
# define and add resources to api

api.add_resource(UserLogin, "/userlogin/")

api.add_resource(UserCollection, "/users/")
api.add_resource(UserItem, "/users/<user_name>/")

api.add_resource(TextCollection, "/texts/")
api.add_resource(TextItem, "/texts/<id>/")

# routes for pagination
api.add_resource(TextItemCount, "/texts/count/")
api.add_resource(TextItemPageCount, "/texts/pages/count/<itemsOnPage>/")
api.add_resource(TextItemsInPages, "/texts/pages/<itemsOnPage>/")

api.add_resource(TextAnnotationCollection, "/textannotations/")
api.add_resource(TextAnnotationItem, "/textannotations/<id>/")