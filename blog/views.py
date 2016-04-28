from flask_blog import app
from flask import render_template, redirect, flash, url_for
from blog.form import SetupForm
from flask_blog import db
from author.models import Author
from blog.models import Blog
from author.decorators import login_required
import bcrypt

@app.route('/')
@app.route('/index/')
def index():
    blogs = Blog.query.count()
    if blogs == 0:
        return redirect(url_for('setup'))
    return "Hello World!"

@app.route('/admin/')
# login_required is a user created decorator; an author decorator
@login_required
def admin():
    return render_template('blog/admin.html')

@app.route('/setup/', methods=['GET', 'POST'])
def setup():
    form = SetupForm()
    error = ""
    if form.validate_on_submit():
        # For secure passwords
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        
        author = Author(
            form.fullname.data,
            form.email.data,
            form.username.data,
            hashed_password, # in place of form.password.data
            True
        )
        db.session.add(author)
        # flush will try to simulate that the record is written to the db to give us the id
        db.session.flush()
        
        if author.id:
            blog = Blog(
                form.name.data,
                author.id
            )
            db.session.add(blog)
            db.session.flush()
        else:
            db.session.rollback()
            error = "Error creating user"
        
        if author.id and blog.id:
            db.session.commit()
            flash("Blog created")
            return redirect(url_for('admin'))
        else:
            db.session.rollback()
            error = "Error creating blog"
            

    return render_template('blog/setup.html', form=form)
