from flask import make_response, request, Flask, jsonify, current_app as current_app
import re
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from datetime import datetime

login = LoginManager()

db = SQLAlchemy()


class Users(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200), unique=True)
    image_file = db.Column(db.String(20), default='default.jpg')
    password = db.Column(db.String(200), unique=True)

    def get_id(self):
           return (self.user_id)

    @login.user_loader
    def load_user(id):
        return Users.query.get(int(id))
    

class Article(db.Model):
    article_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.String(200), db.ForeignKey('users.username'), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
