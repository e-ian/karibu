from flask import Blueprint, make_response, jsonify, request
from app.models import Users
from app.utilities.helpers import jwt_instance

client = Users()

user = Blueprint('user', __name__)

@user.route('/')
def welcome():
    return "Welcome! Karibu!"

@user.route('/auth/register', methods=['POST'])
def create_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    confirm_password = request.json['confirm_password']

    
    if not client.validate_email(email):
        return jsonify(
            {'error': 'email should be in the form someone@example.com', 'status': 400}), 400
    if not client.valid_password(password):
        return jsonify(
            {'error': 'password should be atleast 6 characters, \
                uppercase letters of the alphabet, numbers and cannot have empty spaces', 'status': 400}), 400
    if not client.valid_username(username):
        return jsonify(
            {'error': 'username field should have length of atleast 3 characters, \
            should not have empty spaces, cannot be empty and should contain alphabets', 'status': 400}), 
    if client.confirm_password(password, confirm_password):
        return jsonify(
            {'error': 'Passwords do not match!', 'status': 400}), 400
    check_user = client.check_username(username)
    if check_user:
        return jsonify({'message': 'username already exist', 'status': 400}), 400
    check_email = client.check_email(email)
    if check_email:
        return jsonify({'message': 'email already exists', 'status': 400}), 400

    signup_data = {
        "username": username,
        "email": email,
        "password": password,
        "confirm_password": confirm_password
    }
    client.register_user(signup_data)
    return make_response(jsonify({"message": "User registered successfully", "status": 201}), 201)

@user.route('/auth/login', methods=['POST'])
def sigin_user():
    """ method implementing api for signing in a user """
    data = request.get_json()
    login_data = {
        "email": data.get('email'),
        "password": data.get('password')
    }
    login = client.login_user(login_data)
    if not login:
        return jsonify({'message': 'email doesnot exist', 'status': 404})
    pass_check = client.verify_password(
        login["password"], login_data["password"])
    if login and pass_check:
        access_token = jwt_instance.encode_token(login_data['email'])
        return jsonify({"status": 200, "message": "You are now logged in",
                        "access_token": access_token.decode('UTF-8')}), 200
    else:
        return make_response(
            jsonify({"message": "email or password is wrong", 'status': 400}), 400)
