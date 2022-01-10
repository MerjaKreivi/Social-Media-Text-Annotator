# Meria's Annotator for Social Media Texts
# University of Oulu
# Created by Merja Kreivi-Kauppinen (2021-2022)

# Social-Media-Text-Annotator/HateSpeechAnnotator API config.py

# This file defines configurations and settings for api

# ------------------------------------------------------------------------------------------

import os

# ----------------------------------------------------------------------------------
# get file location, print file location if needed

basedir = os.path.abspath(os.path.dirname(__file__))
# print("\nconfig basedir:  ", basedir)

# -----------------------------------------------------------------------------------
# class Config implements an empty init_app() method

class Config:
    @staticmethod
    def init_app(app):
        pass

# ------------------------------------------------------------------------------------
# Config subclasses define settings for specific configurations
class DevelopmentConfig(Config):
    DEBUG = True    
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, "developmentAnno.db")
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class TestingConfig(Config):
    TESTING = True
    #DEBUG = False
    #SECRET_KEY="dev"    
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, "testingAnno.db")
    #SQLALCHEMY_TRACK_MODIFICATIONS=False

class ProductionConfig(Config):    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'MyManualAnnotations.db')

# config dictionary includes list of available configurations
config = {
'development': DevelopmentConfig,
'testing': TestingConfig,
'production': ProductionConfig,
'default': DevelopmentConfig
}
