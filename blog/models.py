from flask_blog import db, uploaded_images
from datetime import datetime

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    admin = db.Column(db.Integer, db.ForeignKey('author.id'))
    # Set up a relationship between Blog and Post
    posts = db.relationship('Post', backref='blog', lazy='dynamic')
    
    def __init__(self, name, admin):
        self.name = name
        self.admin = admin
        
    def __repr__(self):
        return '<Blog %r>' % self.name

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    image = db.Column(db.String(255))
    # slug is the identifier for the article, e.g. /blog/2015/10/20/sql-alchemy-1.0.9-released/
    # date + title
    slug = db.Column(db.String(256), unique=True)
    publish_date = db.Column(db.DateTime)
    # Set live to false instead of deleting from the database
    live = db.Column(db.Boolean)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    comments = db.relationship('Comment', backref=db.backref('posts', lazy='dynamic'))
    
    # @property means creating a new calculated property of an object
    @property
    def imgsrc(self):
        return uploaded_images.url(self.image)
    
    def __init__(self, blog, author, title, body, category, comments, image=None, slug=None, publish_date=None, live=True):
        self.blog_id = blog.id
        self.author_id = author.id
        self.title = title
        self.body = body
        self.category_id = category.id
        self.comment_id = comments.id
        self.image = image
        self.slug = slug
        if publish_date is None:
            self.publish_date = datetime.utcnow()
        else:
            self.publish_date = publish_date
        self.live = live
        
    def __repr__(self):
        return '<Post %r>' % self.title
        
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        # return '<Category %r>' % self.name
        return self.name

class Comment(db.Model):
    # Need to have a primary key for SQLAlchemy to create the table
    id = db.Column(db.Integer, primary_key=True)
    comment_author = db.Column(db.String(100))
    comment_body = db.Column(db.Text)
    
    # posts = db.relationship('Post', backref='comment', lazy='dynamic')
    
    def __init__(self, comment_author, comment_body):
        self.comment_author = comment_author
        self.comment_body = comment_body

    def __repr__(self):
        return self.name