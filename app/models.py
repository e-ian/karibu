from flask import make_response, request, Flask, jsonify, current_app as current_app
import re
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
# from .database import Database
from werkzeug.security import generate_password_hash, check_password_hash


# db = Database()
# cursor = db.cur
# dictcur = db.dict_cursor

db = SQLAlchemy()


class Users(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200), unique=True)
    

class Article(db.Model):
    article_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(3500))
    created_by = db.Column(db.String(200), db.ForeignKey('Users.username'), nullable=False)


# class Users:

#     def register_user(self, data):
#         query = "INSERT INTO users(username, email, password) \
#             VALUES('{}', '{}', '{}')".format(data['username'], data['email'], \
#                 generate_password_hash(data['password']))
#         cursor.execute(query)
#         return data

#     def validate_email(self, email):
#         if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
#             return False
#         else:
#             return True
    
#     def check_email(self, email):
#         """ method to check if email is already taken """
#         query = "SELECT * FROM users WHERE email='{}'".format(email)
#         dictcur.execute(query)
#         data = dictcur.fetchone()
#         return data
    
#     def valid_username(self, username):
#         """method validating the username input """
#         return isinstance(
#             username,
#             str) and len(username) >= 3 and not re.search(
#             r'\s',
#             str(username)) and not re.search(
#             r'\W',
#             str(username))

#     def check_username(self, username):
#         """ method to check if a username is already taken"""
#         query = "SELECT * FROM users WHERE username='{}'".format(username)
#         dictcur.execute(query)
#         data = dictcur.fetchone()
#         return data


#     def valid_password(self, password):
#         """ method validating the password input """
#         return isinstance(
#             password,
#             str) and len(password) >= 6 and re.search(
#             r'[A-Z]',
#             password) and re.search(
#             r'[0-9]',
#             password) and not re.search(
#                 r'\s',
#             str(password))

#     def confirm_password(self, password, confirm_password):
#         if password != confirm_password:
#             return "passwords do not match"

#     def verify_password(self, data, db_data):
#         return check_password_hash(data, db_data)

#     def login_user(self, data):
#         """ method to login in registered users"""
#         query = "SELECT * FROM users WHERE email='{}'".format(
#             data['email'])
#         dictcur.execute(query)
#         login = dictcur.fetchone()
#         return login

# class Article:

#     def create_article(self, data):
#         query = "INSERT INTO articles(title, content, created_by) \
#             VALUES('{}', '{}', '{}')".format(
#                 data['title'],
#                 data['content'],
#                 data['created_by']
#                 )
#         cursor.execute(query)
#         return data

#     def check_title(self, title):
#         """ check if a title already exists """
#         query = "SELECT * FROM articles WHERE title='{}'".format(title)
#         dictcur.execute(query)
#         data = dictcur.fetchone()
#         return data

#     def get_all_articles(self):
#         query = "SELECT * FROM articles"
#         dictcur.execute(query)
#         articles = dictcur.fetchall()
#         return articles