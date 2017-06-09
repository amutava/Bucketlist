import unittest
import json

from application import create_app, db


class UserTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.context = self.app.app_context()
        self.context.push()
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()
        self.user = {
            "username": "angie",
            "password": "angie"
        }
        
    def test_already_registered_user(self):
        """Tests re-registration."""
        resp = self.client.post('/auth/register',
                                data=json.dumps(self.user),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        res = self.client.post('/auth/register',
                               data=json.dumps(self.user),
                               content_type='application/json')
        self.assertEqual(res.status_code, 409)
        result = json.loads(res.data)
        self.assertEqual(result['message'],
                         "User with the username already exists.")

    def test_registration(self):
        """Tests user registration."""
        response = self.client.post("auth/register",
                                    data=json.dumps(self.user),
                                    content_type="application/json")
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["message"],
                         'User registration successful.')
        self.assertEqual(result['username'],
                         self.user['username'])

    def test_login(self):
        """Tests user login"""
        resp = self.client.post('/auth/register',
                                data=json.dumps(self.user),
                                content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        res = self.client.post('/auth/login',
                               data=json.dumps(self.user),
                               content_type="application/json")
        self.assertEqual(res.status_code, 200)
        result = json.loads(res.data)
        self.assertEqual(result['message'],
                         "Login successful.")
        

    def test_unregistered_user_login(self):
        """Tests unregistered user login."""
        res = self.client.post('/auth/login',
                               data=json.dumps(self.user),
                               content_type="application/json")
        self.assertEqual(res.status_code, 401)
        result = json.loads(res.data)
        self.assertEqual(result['message'],
                         "Invalid username/password.")

    def test_missing_data(self):
        """Tests the user not passing all parameters"""
        res = self.client.post('/auth/login',
                               data=json.dumps({"username": "angie"}),
                               content_type="application/json")
        result = json.loads(res.data)
        self.assertEqual(result['error'],
                         "missing data in request.")

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

if __name__ == '__main__':
    unittest.main()
