import os
import secrets
from PIL import Image
from flask import render_template, redirect, url_for, flash, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

post = [
    {
        'Author':'Nelson Nyamwaro',
        'Title':'How to fish',
        'Date': '24th June 2020'
    },
    {
        'Author':'Richard Smith',
        'Title':'How to cook fish',
        'Date': '25th June 2020'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', post=post)

@app.route('/about')
def about():  
    return render_template('about.html', title='About')

@app.route('/register', methods = ['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully. You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            wanted_page = request.args.get('next')
            login_user(user, remember=form.remember.data)
            return redirect(wanted_page) if wanted_page else redirect(url_for('home'))
        else:
            flash('Failed. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_image(form_image):
    hex_image=secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_image.filename)
    changed_img = hex_image+ file_ext
    img_path = os.path.join(app.root_path, 'static/profilepic', changed_img)
    
    output_size=(125, 125)
    i=Image.open(form_image)
    i.thumbnail(output_size)
    i.save(img_path)
    return changed_img
    
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form=UpdateForm()
    if form.validate_on_submit():
        if form.image.data:
            pic_file=save_image(form.image.data)
            current_user.image=pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email 
    image_file= url_for('static', filename='profilepic/'+ current_user.image)
    return render_template('account.html', title='Account', image_file=image_file, form=form)