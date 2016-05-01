* Rename home directory to blog because have a module for the blog, not home
* MySQL root user: skols75
* CREATE DATABASE blog
* MVC is sometimes called MVT in Flask, Django, etc.
    - Model - The database operations
    - Views - The controllers; the ones that route; views.py
    - Templates - The presentation layer or views

* When creating a new module (or folder), create an __init__.py

* python manage.py runserver
    - Run using this

* python manage.py shell
    - A shell with the application loaded in memory
    - Play with the application this way
    - from flask_blog import db
    - from author.models import Author
        - from author.models import * 
        - imports all classes if there are multiple
            - Might not have to import models with SQLAlchemy
    - db.session.commit()
    - db.create_all()
        - Creates table
    - author = Author(
    'Michael Skolnik', 'michaelskolnik@g.com', 'mike', '12345', True
    )
    - Not in table yet
        - db.session.add(author)
        - db.session.commit()
        - Have to do both after an author is added
    - To interact and query database
        - authors = Author.query.all()
        - authors = Author.query.filter_by(username='mike').first()
        - Then just type authors
    
    - Don't want to continue having data in the tables
    - Use a SQLAlchemy method
        - from flask_blog import db
        - from author.models import *
        - db.session.commit()
            - Do first in case something is waiting to be committed
        - db.drop_all()
            - drops all tables

* flask-wtf
    - Manage forms easily

* @app.route('/webpage/', methods=['GET', 'POST'])
    - GET and POST inside of []

* CSRF Token
    - Makes form hard for hackers to attack with data
    - {{ form.hidden_tag() }}
        - Always use at the beginning of a form

* Macros begin with _
    - _formhelpers.html

* kwargs are keyword arguments
    - (**kwargs)

* Delete cookie to logout manually
    - Firefox is being fucking difficult and not letting me

* Implement something to track database changes instead of trying to do manually
    - flask-migrate
    - Add Migrate to __init__.py of application
        - from flask.ext.migrate import Migrate
        - migrate = Migrate(app,db)
    - Add to manage.py
        - from flask.ext.migrate import MigrateCommand
        - Under manager
            - manager.add_command('db', MigrateCommand)
    - Migrate will take care of creating and initializing tables and also making passwords more secure
        - Drop tables if they exist
    - At command line
        - python manage.py db init
    - Creates a migrations folder
    - Then two more steps you always do at command line
        - python manage.py db migrate
            - Generates the versions folder
        - python manage.py db upgrade
            - Database changes happen, i.e. tables get created

* Secure passwords
    - py-bcrypt
    - Before migration, open env.py in the migrations folder and go to context.configure
        - Add compare_type=True
    - Changes to columns themselves like type or length won't be picked up without that addition
    - username: skittles and password: lunatak

* Create a post in the shell
    - python manage.py shell
    - from author.models import *
    - from blog.models import *
    - category = Category('Python')
    - db.session.add(category)
    - db.session.commit()
    - author = Author.query.first()
        - skittles
    - category = Category.query.first()
    - blog = Blog.query.first()
    - post = Post(blog, author, 'Python is cool!', 'This is why Python is cool. It is the coolest!', category)
    - db.session.add(post)
    - db.session.commit()

* Add python-slugify and flask-markdown to requirements.txt
    - python-slugify allows to generate slugs on the fly without worrying about generating themselves
    - flask-markdown is a library that allows markdowns, which is a formatting utility language to allow edits in posts and make them look like HTML
        - Search for Markdown Cheatsheet
            - https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet

* For TextAreaField, need to add rows to render_field

* Relationships are one to many
    - For every category, there can be multiple posts
    - Put the relationship on the many, i.e. author and posts

* Uploading photos using Flask-Uploads
    - Official currently works with Python 2 only
    - Updated for Python 3 on github
    - Add the following to requirements.txt
        - -e git+https://github.com/fromzeroedu/flask_uploads#egg=flask_uploads
    - Add constants settings.py
        - UPLOADED_IMAGES_DEST = '/home/ubuntu/workspace/app_name/static/images'
        - UPLOADED_IMAGES_URL = '/static/images/'
    - Add to __init__.py
        - from flask_uploads.uploads import UploadSet, configure_uploads, IMAGES
        - uploaded_images = UploadSet('images', IMAGES)
        - configure_uploads(app, uploaded_images)
    - Add to the form tag in post.html
        - enctype="multipart/form-data"

* Editing posts
    - Need to change the form so the image is pre-rendered
    - Make changes to post.html and blog views.py

* Unit testing
    - https://docs.python.org/2/library/unittest.html
    - Concentrate on testing things that relate to the code that was written
    - Try to write tests that cover all uses, including strange things the user might do
    - Check for 1, 2, n scenarios
    - Django has its own built-in testing suite
    - Create tests.py in root of project
    - 