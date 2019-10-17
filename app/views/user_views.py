from flask import Blueprint, make_response, jsonify, request, flash
from app.models import Users, Article
from app.utilities.helpers import jwt_instance
from flask import render_template, redirect, url_for
from app.forms.form import LoginForm, SignupForm

client = Users()

user = Blueprint('user', __name__)

@user.route('/auth/register', methods=['POST', 'GET'])
def create_user():
    form = SignupForm()
    if form.validate_on_submit():
        username=form.username.data
        email=form.email.data
        password=form.password.data
        new_user = {
            "username": username,
            "email": email,
            "password": password
        }
        client.register_user(new_user)
        return redirect(url_for('user.sigin_user'))
    return render_template('register.html', form=form)

@user.route('/auth/login', methods=['POST', 'GET'])
def sigin_user():
    """ method implementing api for signing in a user """
    form = LoginForm(request.form)
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        login_data = {
            "email": email,
            "password": password
        }
        login = client.login_user(login_data)
        if not login:
            flash('Invalid email or password')
        password_check = client.verify_password(login["password"], login_data["password"])
        if login and password_check:
            access_token = jwt_instance.encode_token(login_data['email'])
            print('///', access_token)
            return redirect(url_for('article.create_article'))
        return 'Invalid email or password'
    return render_template('j2_login.html', form=form)
