# Meria's Annotator for Social Media Texts
# University of Oulu
# Created by Merja Kreivi-Kauppinen (2021-2022)

# Social-Media-Text-Annotator/HateSpeechAnnotator API manage.py

# ------------------------------------------------------------------------------------------

# python -m app.manage
# python -m hub.manage

#!/usr/bin/env python
import os
from hub import create_app, db
from hub.models import User, TextContent, TextAnnotation
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

# creates app with defined environment and configuration
app = create_app(os.getenv('FLASK_ENV') or 'default')
with app.app_context():
    db.create_all()

# OR

# Launch Script with code below 
# (from book - Flask Web Development, M. Grinberg, page 81 and 82)
# code below run with command - python manage.py db upgrade

#manager = Manager(app)
#migrate = Migrate(app, db)

#def make_shell_context():
#    return dict(app=app, db=db, User=User, TextContent=TextContent, TextAnnotation=TextAnnotation)
#manager.add_command("shell", Shell(make_context=make_shell_context))
#manager.add_command('db', MigrateCommand)

#if __name__ == '__main__':
#    manager.run()