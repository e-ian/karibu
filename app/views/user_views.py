from flask import Blueprint, make_response, jsonify, request, flash
from app.models import Users, Article
from app.utilities.helpers import jwt_instance
from flask import render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from app.forms.form import LoginForm, SignupForm
from app import db

# client = Users()

user = Blueprint('user', __name__)

# @user.route('/')
# def welcome():
#     return render_template("welcome")

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
        # client.register_user(new_user)
        return redirect(url_for('user.sigin_user'))
    return render_template('register.html', form=form)

@user.route('/auth/login', methods=['POST', 'GET'])
def sigin_user():
    """ method implementing api for signing in a user """
    form = LoginForm(request.form)
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        # login_data = {
        #     "email": email,
        #     "password": password
        # }
        # login = client.login_user(login_data)
        user = Users.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password')
            return render_template('j2_login.html', form=form)
        # password_check = client.verify_password(login["password"], login_data["password"])
        # if login and password_check:
            # access_token = jwt_instance.encode_token(login_data['email'])
            # print('///', access_token)
            # return redirect(url_for('article.create_article'))
        # return 'Invalid email or password'  
        login_user(user, remember=False)
        return redirect(url_for('article.create_article'))
    return render_template('j2_login.html', form=form)
    