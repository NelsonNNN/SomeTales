import os
import secrets
from PIL import Image
from flask import render_template, redirect, url_for, flash, request, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateForm, UpdatePost
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required



@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    post=Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
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

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form=UpdatePost()
    if form.validate_on_submit():
        flash('Your post has been created', 'success')
        post = Post(title=form.title.data, content=form.content.data, author=current_user )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('posts.html', title='Post', form=form, legend='New Post')

@app.route('/post/<int:post_id>')
def edit_post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('editpost.html', post=post)

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = UpdatePost()     
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data      
        db.session.commit()
        flash('Post has been updated successfully', 'success')
        return redirect(url_for('edit_post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('posts.html', form=form, post=post, legend='Update Post')

@app.route('/post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted', 'success')
    return redirect(url_for('home'))

@app.route('/user/<string:username>')
def user_page(username):
    page = request.args.get('page', 1, type=int)
    user= User.query.filter_by(username=username).first_or_404()
    post = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('user.html', user=user, post=post)