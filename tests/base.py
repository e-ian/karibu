"base tests"
import unittest
import json
from app import create_app
from config import TestingConfig
from . import (create_user, signin_user, create_article)
from app.database import Database

app = create_app('testing')
db = Database()

class TestUser(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.db = Database()

    def tearDown(self):
        self.db.cur.execute("DROP TABLE users CASCADE")

    "base tests for user authentication"

    def register_user(self, create_user):
        response = self.client.post(
            '/auth/register',
            data=json.dumps(create_user),
            content_type='application/json'
        )
        return response

    def signin_user(self):
        self.register_user(create_user)
        response = self.client.post(
            '/auth/login',
            data=json.dumps(signin_user),
            content_type='application/json')
        data = json.loads(response.data.decode())
        return data

    def create_article(self, create_article):
        response = self.client.post(
            '/article',
            data=json.dumps(create_app),
            content_type='application/json',
            headers=self.user_header()
        )
        return response

    def user_header(self):
        return{
            'content_type': 'application/json',
            'Authorization': self.signin_user()['access_token']
            }

    def get_articles(self):
        response = self.client.get(
            '/article/all',
            headers=self.user_header() 
        )
        return response
