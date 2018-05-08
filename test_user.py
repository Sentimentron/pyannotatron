from unittest import TestCase
from pyannotatron.models import NewUserRequest, UserKind, LoginResponse


class TestNewUserRequest(TestCase):

    def test_to_json(self):
        n = NewUserRequest(username="roger", email="admin@company.com", role=UserKind.ADMINISTRATOR, password="floogity")
        ref = {
            "username": "roger",
            "email": "admin@company.com",
            "role": "Administrator",
            "password": "floogity"
        }
        self.assertDictEqual(n.to_json(), ref)

    def test_from_json(self):
        ref = {
            "username": "roger",
            "email": "annotator@company.com",
            "role": "Annotator",
            "password": "floogity"
        }
        n = NewUserRequest.from_json(ref)
        self.assertEqual(n.username, "roger")
        self.assertEqual(n.email, "annotator@company.com")
        self.assertEqual(n.role, UserKind.ANNOTATOR)
        self.assertEqual(n.password, "floogity")


class TestLoginResponse(TestCase):

    def test_to_json(self):
        n = LoginResponse(token="blasdfasdf", password_reset_needed=False)
        ref = {
            "token": "blasdfasdf",
            "passwordResetNeeded": False
        }
        self.assertDictEqual(n.to_json(), ref)

    def test_from_json(self):
        ref = {
            "token": "blasdfasdf",
            "passwordResetNeeded": True
        }
        n = LoginResponse.from_json(ref)
        self.assertEqual(n.token, "blasdfasdf")
        self.assertTrue(n.password_reset_needed)