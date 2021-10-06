from datetime import datetime
import os
import secrets
from flaskblog import app, mongo
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, session
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
import bcrypt
from bson import ObjectId


def ran(x):
    return range(int(x))


app.jinja_env.filters['ran'] = ran


@app.route('/')
def home():
    check = 0
    if 'username' in session:
        check = 1
    a = []
    b = []
    c = []
    reviews = mongo.db['reviews'].find({})

    for idx, val in enumerate(reviews):
        if idx < 4:
            a.append(val)
        elif idx < 9:
            b.append(val)
        elif idx < 14:
            c.append(val)
        print(a)
    print(a)
    return render_template('home.html', check=check, reviews=reviews, a=a, b=b, c=c)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        users = mongo.db.users
        if form.validate_on_submit():
            hashpass = bcrypt.hashpw(
                form.password.data.encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': form.username.data,
                          'password': hashpass, 'email': form.email.data})
            session['username'] = request.form['username']
            return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'name': form.username.data})
        if login_user:
            if bcrypt.hashpw(form.password.data.encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = form.username.data
                return redirect(url_for('home'))
        flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route("/file/<filename>")
def file(filename):
    return mongo.send_file(filename)


@app.route("/account", methods=['GET', 'POST'])
def account():
    form = UpdateAccountForm()
    users = mongo.db.users
    user = users.find_one({'name': session['username']})
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.picture.data:
                profile_image = form.picture.data
                mongo.save_file(profile_image.filename, profile_image)
                users.find_one_and_update({'name': session['username']}, {"$set": {
                    'profile_image_name': profile_image.filename
                }})

            users.find_one_and_update({'name': session['username']}, {"$set": {
                'name': form.username.data,
                'email': form.email.data
            }})
            session.clear()
            session['username'] = form.username.data
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))
    form.username.data = user['name']
    form.email.data = user['email']
    try:
        user['profile_image_name']
        image_file = url_for('file', filename=user["profile_image_name"])
    except:
        image_file = ''
    return render_template('account.html', title='Account',
                           user=user, form=form, profile_image=image_file)


@app.route("/give-review", methods=['GET', 'POST'])
def new_review():
    form = PostForm()
    reviews = mongo.db.reviews
    if form.validate_on_submit():
        reviews.insert({'title': form.title.data,
                        'link': form.link.data, 'review': form.review.data,
                        'content': form.content.data,
                        'star': request.form['star'], 'author': session['username'], 'created_at': datetime.utcnow()})
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_review.html', title='New Review',
                           form=form,)


@app.route("/reviews")
def reviews():
    reviews = mongo.db['reviews'].find({})
    return render_template('reviews.html', reviews=reviews)


@app.route("/review_show/<string:review_id>", methods=['GET'])
def review_show(review_id):
    users = mongo.db.reviews
    review = users.find_one({'_id': ObjectId(review_id)})
    print(review)
    return render_template('review_show.html', review=review)
