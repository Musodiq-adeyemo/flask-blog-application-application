from fileinput import filename
from werkzeug.utils import secure_filename
from io import BytesIO
from urllib.request import AbstractBasicAuthHandler
from flask import Blueprint, send_file, url_for,render_template,redirect,request,flash,Response
from flask_login import login_user, login_required,logout_user,current_user
from . import db,mail,Message
from sqlalchemy.sql import func 
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User,Img
import os

auth = Blueprint('auth',__name__)

# Registration route(This is used to register user by getting their info )
@auth.route('/register', methods=['POST','GET'])
def register():
    if request.method =='POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        phone = request.form.get('phone')
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        gender = request.form.get('gender')

        user = User.query.filter_by(email=email).first()
        username_exist = User.query.filter_by(username=username).first()

        if user :
            flash('Email address already exist.',category='error')
            return redirect(url_for('auth.login'))
        elif username_exist:
            flash('Username already in use try another one.',category='error')
        elif password1 != password2:
            flash('password don/t match.Try again',category='error')
        elif len(username) < 8:
            flash('Username to short atleast 8 characters.',category='error')
        else :
            new_user = User(firstname=firstname,lastname=lastname,phone=phone,email=email,username=username,password1=generate_password_hash(password1,method='sha224'),gender=gender)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('Account successfully created.please login',category='success')
            return redirect(url_for('auth.login'))
    return render_template('register.html')

# login User route(This is used to login user by getting their info )
@auth.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST' :
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password1,password):
                flash('You have been logged in Successfully.',category='success')
                login_user(user,remember=True)
                return redirect(url_for('main.home'))
            else:
                flash('Password is incorrect.',category='error')
        else:
            flash('Email does not exist.Please register first',category='error')
            return redirect(url_for('auth.register'))

    return render_template('login.html')
                
#logout User route(This is used to logout user by getting their info )
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# contact page route(This is used to send user message to the admin )
@auth.route('/contact', methods=['POST','GET'])
def contact():
    if request.method =='POST':
        email = request.form.get('email')
        username = request.form.get('username')
        phone = request.form.get('phone')
        message = request.form.get('message')

        msg= Message(subject=f"Mail from{username}",body=F"Username:{username}\nEmail:{email}\n phone:{phone}\n\n\n Message:{message}",sender= current_user.email,recipients=["sirmuso@gmail.com"])
        mail.send(msg)
        flash("Your message has been sent Successfully",category='success')

    return render_template("contact.html")

#This is the dashboard route for uploading a file
@auth.route('/upload', methods=['GET','POST'])
@login_required
def upload_image():
    if request.method == "POST":
        if 'pic' not in request.files:
            flash("No file part",category='error')
            return redirect(request.url)
        pic = request.files['pic']
        if pic.filename=='':
            flash("No file selected for uploading",category='error')
            return redirect(request.url)
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype

        image_upload = Img(img = pic.read(),mimetype=mimetype, name=filename)
        db.session.add(image_upload)
        db.session.commit()
        flash("Your profile picture has been successfully uploaded",category='success')
        return redirect('/dashboard')

    return render_template("dashboard.html")

@auth.route('/upload/<int:id>')
@login_required
def get_img(id):
    image = Img.query.filter_by(id=id).first()
    if image is None:
        return "No image with that id"
    return Response(image.img,mimetype=image.mimetype)



#this is used for downloading user profile pic
@auth.route('/dashboard/download/<user_id>')
def download_image(user_id):
    download = User.query.filter_by(id=user_id).first()

    return send_file(BytesIO(download.data), attachment_filename = User.image, as_attachment=True)

#This is the dashboard page route
@auth.route('/dashboard')
@login_required
def dashboard():
    
    return render_template("dashboard.html")

#This route is used to delete the user profile
@auth.route('/dashboard/delete/<int:id>')
def delete_profile(id):
    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()
    flash("Your profile has been deleted successfully.", category="success")
    return redirect('/dashboard')

#This route is used to update the user profile
@auth.route('/dashboard/update/<int:id>',methods=['GET','POST'])
def update_profile(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        phone = request.form.get('phone')
        email = request.form.get('email')
        username = request.form.get('username')
        gender = request.form.get('gender')

        current_user.firstname = firstname
        current_user.lastname = lastname
        current_user.phone = phone
        current_user.email = email
        current_user.username= username
        current_user.gender = gender
        
        db.session.commit()
        flash("Your profile has been updated successfully.", category="success")
        return redirect(url_for('auth.dashboard'))
    return render_template('profile_update.html', user=user)