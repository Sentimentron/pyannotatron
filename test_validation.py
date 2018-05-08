from unittest import TestCase
from pyannotatron.models import FieldError, ValidationError


class TestFieldError(TestCase):

    def test_to_json(self):
        fe = FieldError("field", "not filled in", True)
        ref = {
            "name": "field",
            "error": "not filled in",
            "warning": True
        }
        self.assertDictEqual(fe.to_json(), ref)

    def test_from_json(self):
        ref = {
            "name": "field",
            "error": "not filled in",
            "warning": True
        }
        fe = FieldError.from_json(ref)
        self.assertEqual(fe.name, "field")
        self.assertEqual(fe.error, "not filled in")
        self.assertTrue(fe.warning)


class TestValidationError(TestCase):
    def test_to_json(self):
        fe1 = FieldError("field", "not filled in", True)
        fe2 = FieldError("email", "obviously wrong", False)
        ve = ValidationError([fe1, fe2])
        ref = [{
            "name": "field",
            "error": "not filled in",
            "warning": True
        }, {
            "name": "email",
            "error": "obviously wrong",
            "warning": False
        }]

        self.assertEqual(ve.to_json(), ref)

    def test_from_json(self):
        ref = [{
            "name": "field",
            "error": "not filled in",
            "warning": True
        }]
        ve = ValidationError.from_json(ref)
        fe = ve.errors[0]
        self.assertEqual(fe.name, "field")
        self.assertEqual(fe.error, "not filled in")
        self.assertTrue(fe.warning)