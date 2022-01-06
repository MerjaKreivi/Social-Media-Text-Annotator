# PWP course 2021 University of Oulu
# created by Merja Kreivi-Kauppinen

# Hate speech Annotator API - api_routes.py
# ------------------------------------------------------------------------

from flask import Blueprint
from flask_restful import Api

# import hub.resources
from hub.resources import UserItem, UserCollection, UserLogin
from hub.resources import TextItem, TextCollection, TextItemCount, TextItemPageCount
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
api.add_resource(TextItemCount, "/texts/count/")
api.add_resource(TextItemPageCount, "/texts/pages/count/<itemsOnPage>/")

api.add_resource(TextAnnotationCollection, "/textannotations/")
api.add_resource(TextAnnotationItem, "/textannotations/<id>/")


# ----------------------------------------------------------
# define routes

"""
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""
# new start
"""
@app.route("/api/")
def entry_point():
    
    body = MasonBuilder()
    body.add_namespace("annometa", "/api/")
    body.add_control("annometa:users-all", "/api/users/")
    return Response(json.dumps(body), mimetype=MASON)

@app.route(LINK_RELATIONS_URL)
def send_link_relations():
    return "link relations"

@app.route("/profiles/<profile>/")
def send_profile(profile):
    return "you requests {} profile".format(profile)


@app.route("/admin/")
def admin_site():
    return app.send_static_file("html/admin.html")
"""
# 
# --------------------------------------------------------------