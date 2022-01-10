# Meria's Annotator for Social Media Texts
# University of Oulu
# Created by Merja Kreivi-Kauppinen (2021-2022)

# Social-Media-Text-Annotator/HateSpeechAnnotator API setup.py
# This file initializes RESTful web flask app

# ------------------------------------------------------------------------------------------

# In order to run tests project need to be installed so that it can be found from the virtual environment's path
# Python packages are installed with setup script

# package name = hub
# package version = 0.1.0

# packages=find_packages()
# include_package_data = True
# To include package data - as static files: HTML, CSS, JS, JSON schemas, pictures etc. that are in static folder. 
# In order for them to be included they also need to be listed in a file called MANIFEST.in.

# requirements.txt file can be created with command
# (.venv) C:\Social-Media-Text-Annotator\HateSpeechAnnotator>pip freeze
# (.venv) C:\Social-Media-Text-Annotator\HateSpeechAnnotator>pip freeze > requirements.txt

from setuptools import find_packages, setup

setup(
    name="HateSpeechAnnotator",
    version="0.1.0",
    author="Merja Kreivi-Kauppinen",
    url="https://github.com/MerjaKreivi/Social-Media-Text-Annotator/HateSpeechAnnotator/",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
        "flask-restful",
        "flask-sqlalchemy",
        "SQLAlchemy",
        "pysqlite3",
        "pytest",
        "pytest-cov",
        "Flask-Script",
        "Flask-Migrate",
        "Pillow",
        "jsonschema",
        "requests",
        "click",
        "itsdangerous",
        "Jinja2",
        "Markupsafe",
        "Werkzeug"
    ]
)

"""
"alembic",
"aniso8601",
"atomicwrites",
"attrs",
"colorama",
"coverage",
"greenlet",
"iniconfig",
"Mako",
"packaging",
"pluggy",
"py",
"pyparsing",
"pyrsistent",
"python-dateutil",
"python-editor",
"pytz",
"six",
"toml"
"""