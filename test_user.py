from unittest import TestCase
from pyannotatron.models import NewUserRequest, UserKind


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

