import os, sys
# Allows python to know starting point of the app and then find other files and folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server
from flask.ext.migrate import MigrateCommand
from flask_blog import app

manager = Manager(app)
manager.add_command('db', MigrateCommand)

manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = os.getenv('IP', '0.0.0.0'),
    port = int(os.getenv('PORT',5000))
    )
)

if __name__ == "__main__":
    manager.run()
