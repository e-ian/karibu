import os
import secrets
from PIL import Image
from flask import Blueprint, make_response, jsonify, request, flash
from app.models import Users, Article
from flask import render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from app.forms.form import LoginForm, SignupForm, UpdateAccountForm
from app import db, create_app as create_app


user = Blueprint('user', __name__)

@user.route('/auth/register', methods=['POST', 'GET'])
def create_user():
    form = SignupForm()
    if form.validate_on_submit():
        username=form.username.data
        email=form.email.data
        password=form.password.data
        new_user = Users(
            username=username,
            email=email,
            password=generate_password_hash(password, method='sha256')
        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user.sigin_user'))
    return render_template('register.html', form=form)

@user.route('/auth/login', methods=['POST', 'GET'])
def sigin_user():
    """ method implementing api for signing in a user """
    form = LoginForm(request.form)
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        user = Users.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password')
            return render_template('j2_login.html', form=form)
        login_user(user, remember=False)
        return redirect(url_for('article.get_articles'))
    return render_template('j2_login.html', form=form)
    
@user.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('article.get_articles'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(create_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@user.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('user.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)
