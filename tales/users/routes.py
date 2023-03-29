from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from tales import db, bcrypt
from models import User, Post
from users.forms import RegistrationForm, LoginForm, UpdateForm, ResetRequest, ResetPassword
from users.utils import save_image, send_reset_email

users = Blueprint('users', __name__)

@users.route('/register/', methods = ['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully. You can now log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Registration', form=form)

@users.route('/login/', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            wanted_page = request.args.get('next')
            login_user(user, remember=form.remember.data)
            return redirect(wanted_page) if wanted_page else redirect(url_for('main.home'))
        else:
            flash('Failed. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('users.login'))
    
@users.route('/account/', methods=['GET', 'POST'])
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
        flash('Account details have been updated successfully')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email 
    image_file= url_for('static', filename='profilepic/{}'.format(current_user.image))
    return render_template('account.html', title='Account', image_file=image_file, form=form)



@users.route('/user/<string:username>/')
def user_page(username):
    page = request.args.get('page', 1, type=int)
    user= User.query.filter_by(username=username).first_or_404()
    post = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('user.html', user=user, post=post)

@users.route('/password_reset/', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ResetRequest()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Check your email for the link to reset your password')
        return redirect(url_for('users.login'))
    return render_template('request_token.html', title='Password Reset Request', form=form)

@users.route('/reset_password/<token>/', methods = ['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('The token is currently expired. Please make a new request.', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPassword()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pwd
        db.session.commit()
        flash('Your password has been updated. You can now log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)