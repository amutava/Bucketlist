import os
import unittest
import json

from flask import Flask
from flask_httpauth import HTTPTokenAuth

from .. auth.models import db, User
from app import create_app, db


class UserTest(unittest.TestCase):

    def setUp():
        self.app = create_app(config_name="testing")
        self.ctx = self.app.app_context()
        self.client = self.app.test_client()
        self.ctx.push()
        db.drop_all()
        db.create_all()
        self.user = {
        "username" : "angie",
        "password": "angie"
        }

    def test_registration(self):
        resp = self.client.post('/auth/register/', data=self.user)
        result = json.losds(resp.data.decode('utf-8').\
            replace("'", "\""))
        self.assertEqual(result['message'], "User registration successful.")
        self.assertEqual(resp.status_code, 201)

    def test_already_registered_user(self):
         resp = self.client.post('/auth/register/', data=self.user)   
         self.assertEqual(resp.status_code, 201)
         res = self.client.post('/auth/register/', data=self.user)  
         self.assertEqual(res.status_code, 202)
         result = json.losds(res.data.decode('utf-8').\
            replace("'", "\""))
         self.assertEqual(result['message'], "User already registered.")

    def test_login(self):
         resp = self.client.post('/auth/register/', data=self.user)   
         self.assertEqual(resp.status_code, 201)
         res = self.client.post('/auth/login/', data=self.user)  
         result = json.losds(res.data.decode('utf-8').\
            replace("'", "\""))
         self.assertEqual(result['message'], "Login successful.")
         self.assertEqual(res.status_code, 200)

    def test_unregistered_user_login(self):      
        res = self.client.post('/auth/login/', data=self.user)  
        self.assertEqual(res.status_code, 401)
        result = json.losds(res.data.decode('utf-8').\
            replace("'", "\""))
        self.assertEqual(result['message'], "Invalid username/ password.")

    def tearDown():
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

if __name__ == '__main__':
    unittest.main()     
