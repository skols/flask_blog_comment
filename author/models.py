from flask_blog import db

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80))
    email = db.Column(db.String(65), unique=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(60))
    # Author that can post to blog or comment only; True if post to blog
    is_author = db.Column(db.Boolean)
    
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # What happens when object is first defined
    def __init__(self, fullname, email, username, password, is_author=False):
        self.fullname = fullname
        self.email = email
        self.username = username
        self.password = password
        self.is_author = is_author
    
    # How to display when iteracting in the terminal
    def __repr__(self):
        return '<Author %r>' % self.username
