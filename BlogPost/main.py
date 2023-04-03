from flask import Blueprint, abort, render_template,redirect,url_for,request,flash, abort
from flask_login import login_required,current_user
from . import db
from sqlalchemy.sql import func 
import os
from .models import BlogPost,User

# Blueprint from flask package is used to for my main file
main = Blueprint('main',__name__)

#This is the route to about page
@main.route('/about')
def about():
    return render_template('about.html')

# This is the route to the homepage where all posts appear 
@main.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content = post_content, author = post_author,poster_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
       
        flash("Your post has been created successfully.", category="success")
        return redirect('/')
    else:
        all_posts =BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    
    return render_template('home.html', post=all_posts)

 # This route is used for delecting post 
@main.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)

    # Only the owner of the post can update their post
    if current_user.id == post.poster_id:

        db.session.delete(post)
        db.session.commit()
        flash("Your post has been deleted successfully.", category="success")
        return redirect('/')
    else:
        flash("You are not authorized to delete this post...",category="error")
        return redirect('/')

# This route is used for updating Posts
@main.route('/posts/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        post_title = request.form.get('title')
        post_content = request.form.get('content')
        
        # Only the owner of the post can update their post 
        if current_user.id == post.poster_id:

            post.title = post_title
            post.content = post_content

            db.session.commit()
            flash("Your post has been updated successfully.", category="success")
            return redirect('/')
        else:
            flash("You are not authorized to update this post...",category="error")
            return redirect('/')
    else :
        return render_template('edit.html', posts=post)

#This route is used for creating new posts
@main.route('/posts/new_posts', methods=['GET','POST'])
@login_required
def new_posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content = post_content, author = post_author,poster_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')
        
    
    else :
        return render_template('new_post.html')

#This route is used for getting post by their id
@main.route("/search", methods=['POST','GET'])
@login_required
def get_post_id():

    post_id = request.form.get('post_id')
    
    if post_id:
        post=BlogPost.query.filter(BlogPost.id.contains(post_id))
        flash("Your post has been retrieved successfully.", category="success")
    else:
        post=BlogPost.query.all()
        
    return render_template('search.html',post=post)

#This route is used for getting post by their title
@main.route("/search", methods=['POST','GET'])
@login_required
def get_post_by_user():

    user_id = request.form.get('user_id')
    
    if user_id:
        post=BlogPost.query.filter(BlogPost.poster_id.contains(user_id))
        flash("Your post has been retrieved successfully.", category="success")
    else:
        post=BlogPost.query.all()
        
    return render_template('search.html',post=post)

#This route is used for getting post by their author name
@main.route("/search", methods=['POST','GET'])
@login_required
def get_post_by_current_user():

    current_user_id = request.form.get('current_user_id')
    
    if current_user_id:
        post=BlogPost.query.filter(BlogPost.poster_id.contains(current_user_id))
        flash("Your post has been retrieved successfully.", category="success")
    else:
        post=BlogPost.query.all()
        
    return render_template('search.html',post=post)


#This is the route for the admin page
@main.route('/admin')
@login_required
def admin():
    # only user with id 1 can view this page
    id = current_user.id
    if id == 1:
        return render_template("admin.html")
    else:
        flash("Please you are not authorized to view this page.Admin only",category="error")
        return redirect(url_for('main.home'))

# This is the route for viewing each post content
@main.route('/<int:id>')
def post(id):
    
    posts = BlogPost.query.get_or_404(id)

    return render_template('content.html',post=posts)

#This route is used to delete the admin profile
@main.route('/admin/delete/<int:id>')
def delete_profile(id):
    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()
    flash("Your profile has been deleted successfully.", category="success")
    return redirect('/admin')

#This route is used to update the admin profile
@main.route('/admin/update/<int:id>',methods=['GET','POST'])
def update_profile(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        username = request.form.get('username')
        gender = request.form.get('gender')

        firstname = firstname
        lastname = lastname
        phone = phone
        email = email
        username= username
        gender = gender
        
        db.session.commit()
        flash("Your proile has been updated successfully.", category="success")
        return redirect('admin.html')
    return render_template('profile_update.html', user=user)