from functools import wraps
from flask import jsonify, request, current_app as app
import jwt
import datetime
from app.models import Users

client = Users()

class Secure_jwt:
    SECRET = 'akokoro'

    def encode_token(self, email):
        """method to generate token """

        payload = {
            'user': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        }
        return jwt.encode(payload, 'akokoro', algorithm='HS256')

jwt_instance = Secure_jwt()

def protected(f):
    """Decorator for protecting routes"""
    @wraps(f)
    def decorator(*args, **kwargs):
        access_token = None
        print(request.headers)
        if 'Authorization' in request.headers:
            access_token = request.headers['Authorization']
            if not access_token:
                return jsonify(
                    {'status': 401, 'error': 'Missing authorization token'}), 401
        else:
            return jsonify(
                    {'status': 400, 'error': 'Missing authorization header'}), 400

        try:
            payload = jwt.decode(access_token, 'akokoro', algorithms=['HS256'])
            logged_user = client.check_email(payload['user'])
        except jwt.ExpiredSignatureError:
            return jsonify(
                {'status': 401, 'error': 'Access token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify(
                {'status': 401, 'error': 'Access token is invalid'}), 401
        return f(logged_user, *args, **kwargs)
    return decorator
