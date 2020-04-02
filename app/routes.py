from flask import render_template, redirect, url_for, flash
from app import app
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post

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
    if form.validate_on_submit():
        flash(f'Account created successfully for { form.username.data }', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Registration', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'nelson@gmail.com' and form.password.data == 'nelliville51':
            return redirect(url_for('home'))
        else:
            flash('Failed. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)