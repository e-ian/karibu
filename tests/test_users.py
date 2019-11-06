from .base import TestUser
from . import (create_user, signin_user)

class TestApp(TestUser):
    
    def test_register_user(self):
        response = self.register_user(create_user)
        self.assertIn("User registered successfully", str(response.data))

    def test_login(self):
        self.register_user(create_user)
        response = self.signin_user()
        self.assertIn(response['message'], 'You are now logged in')
