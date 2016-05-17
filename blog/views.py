from flask_blog import app
from flask import render_template, redirect, flash, url_for, session, abort, request
from blog.form import SetupForm, PostForm, CommentForm
from flask_blog import db, uploaded_images
from author.models import Author
from blog.models import Blog, Category, Post, Comment
from author.decorators import login_required, author_required
import bcrypt
from slugify import slugify

# Constant to set posts per page
POSTS_PER_PAGE = 5

@app.route('/')
@app.route('/index/')
# Page number
@app.route('/index/<int:page>')
def index(page=1):
    blog = Blog.query.first()
    if not blog:
        return redirect(url_for('setup'))
    # If page doesn't exist, returns 404 if set to True
    # With False, returns empty list instead
    posts = Post.query.filter_by(live=True).order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('blog/index.html', blog=blog, posts=posts)

@app.route('/admin/')
@app.route('/admin/<int:page>')
# author_required is a user created decorator; an author decorator
@author_required
def admin(page=1):
    if session.get('is_author'):
        posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
        return render_template('blog/admin.html', posts=posts)
    else:
        # return a 403 error message, which means forbidden
        abort(403)

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
            return redirect(url_for('index'))
        else:
            db.session.rollback()
            error = "Error creating blog"
            

    return render_template('blog/setup.html', form=form)

@app.route('/post/', methods=['GET', 'POST'])
@author_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        image = request.files.get('image')
        filename = None
        try:
            filename = uploaded_images.save(image)
        except:
            flash("The image was not uploaded.")
        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            category = new_category
        elif form.category.data:
            category_id = form.category.get_pk(form.category.data)
            category = Category.query.filter_by(id=category_id).first()
        else:
            category = None
        blog = Blog.query.first()
        # BE SURE TO INCLUDE first()
        author = Author.query.filter_by(username=session['username']).first()
        title = form.title.data
        body = form.body.data
        slug = slugify(title)
        post = Post(blog, author, title, body, category, filename, slug)
        post.save()
        return redirect(url_for('article', slug=slug))
        
    return render_template('blog/post.html', form=form, action="new")

# slug is unique, so works for an id
# @app.route('/article/<slug>/', methods=['GET', 'POST'])
# def article(slug):
#     post = Post.query.filter_by(slug=slug).first_or_404(id)
#     form = CommentForm()
#     if form.validate_on_submit():
#         comment_author = form.comment_author.data
#         comment_body = form.comment_body.data
#         post_id = post.id
#         comment = Comment(post_id, comment_author, comment_body)
#         # form.populate_obj(comment)
#         # db.session.add(comment)
#         # db.session.commit()
#         post.comments.append(comment)
#         db.session.add(post)
#         db.session.commit()
#         return redirect(url_for('article', slug=slug))
#     return render_template('blog/article.html', form=form, post=post)

@app.route('/article/<int:post_id>/', methods=['GET', 'POST'])
def article(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    form = CommentForm()
    if form.validate_on_submit():
        comment_author = form.comment_author.data
        comment_body = form.comment_body.data
        post_id = post.id
        comment = Comment(post_id, comment_author, comment_body)
        db.session.add(comment)
        # db.session.commit()
        post.comments.append(comment)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('article', post_id=post.id))
    comments=Comment.query.all()
    return render_template('blog/article.html', form=form, post=post, comments=comments)


# @app.route('/article/<slug>/comment', methods=['GET', 'POST'])
# def comment(slug):
#     post = Post.query.filter_by(slug=slug).first_or_404()
#     form = CommentForm()
#     if form.validate_on_submit():
#         comment_author = form.comment_author.data
#         comment_body = form.comment_body.data
#         comment = Comment(comment_author, comment_body)
#         db.session.add(comment)
#         db.session.commit()
#         return redirect(url_for('article', slug=slug))
#     return render_template('blog/article.html', form=form, post=post)


@app.route('/edit/<int:post_id>',methods=['GET','POST'])
@author_required
def edit(post_id):
    # Return post form, but filled out
    # Use existing PostForm
    post = Post.query.filter_by(id=post_id).first_or_404()
    form = PostForm(obj=post) # post here is the post in previous line; fills out the form with that data
    if form.validate_on_submit():
        original_image=post.image
        form.populate_obj(post) # Replaces post with the contents of the form
        if form.image.has_file():
            image = request.files.get('image')
            try:
                filename = uploaded_images.save(image)
            except:
                flash("The image was not uploaded.")
            if filename:
                post.image=filename
        else:
            post.image = original_image
        
        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            post.category = new_category
        db.session.commit()
        return redirect(url_for('article', slug=post.slug))
    return render_template('blog/post.html', form=form, post=post, action="edit")

@app.route('/delete/<int:post_id>')
@author_required
def delete(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.live = False
    db.session.commit()
    flash("Article deleted.")
    return redirect('/admin/')
