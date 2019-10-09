from flask import make_response, request, Flask, jsonify, current_app as current_app
import re
from .database import Database
from werkzeug.security import generate_password_hash, check_password_hash

db = Database()
cursor = db.cur
dictcur = db.dict_cursor

class Users:

    def register_user(self, data):
        query = "INSERT INTO users(username, email, password) \
            VALUES('{}', '{}', '{}')".format(data['username'], data['email'], \
                generate_password_hash(data['password']))
        cursor.execute(query)
        return data

    def validate_email(self, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False
        else:
            return True
    
    def check_email(self, email):
        """ method to check if email is already taken """
        query = "SELECT * FROM users WHERE email='{}'".format(email)
        dictcur.execute(query)
        data = dictcur.fetchone()
        return data
    
    def valid_username(self, username):
        """method validating the username input """
        return isinstance(
            username,
            str) and len(username) >= 3 and not re.search(
            r'\s',
            str(username)) and not re.search(
            r'\W',
            str(username))

    def check_username(self, username):
        """ method to check if a username is already taken"""
        query = "SELECT * FROM users WHERE username='{}'".format(username)
        dictcur.execute(query)
        data = dictcur.fetchone()
        return data


    def valid_password(self, password):
        """ method validating the password input """
        return isinstance(
            password,
            str) and len(password) >= 6 and re.search(
            r'[A-Z]',
            password) and re.search(
            r'[0-9]',
            password) and not re.search(
                r'\s',
            str(password))

    def confirm_password(self, password, confirm_password):
        if password != confirm_password:
            return "passwords do not match"

    def verify_password(self, data, db_data):
        return check_password_hash(data, db_data)

    def login_user(self, data):
        """ method to login in registered users"""
        query = "SELECT * FROM users WHERE email='{}'".format(
            data['email'])
        dictcur.execute(query)
        login = dictcur.fetchone()
        return login

    