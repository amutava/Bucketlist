import os
import unittest
import json

from flask import Flask
from flask_httpauth import HTTPTokenAuth

from application.auth.models import User
from application import create_app, db


class BucketListTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.ctx = self.app.app_context()
        self.client = self.app.test_client()
        self.ctx.push()
        db.drop_all()
        db.create_all()
        self.user ={
                    "username":"angie", 
                    "password":"angie"
                    }
        self.added_user = User(self.user["username"], 
            self.user["password"])
        db.session.add(self.added_user)
        db.session.commit()
        user = User.query.filter_by(username = 'angie').first()
        self.bucketlist = {
                        'name': 'Go to Canada.', 
                        'description':"with an helicopter."
                        }
        self.token = user.generate_auth_token(user.id)

    def test_create_bucketlist(self):
        """ Tests bucketlist creation."""
        resp = self.client.post('/bucketlists', 
            data=json.dumps(self.bucketlist), 
            content_type= "application/json", headers={
            "Authorization":self.token
            })
        self.assertEqual(resp.status_code, 201)
        result = json.loads(resp.data)
        self.assertEqual(result['message'], 
            "Bucketlist created successfully.")
        self.assertEqual(result['name'], 
            'Go to Canada.')
        self.assertEqual(result['description'], 
            "with an helicopter.")

    def test_invalid_token(self):
        """Test user providing an invalid token."""
        resp = self.client.post('/bucketlists', 
            data=json.dumps(self.bucketlist), 
            content_type= "application/json", headers={
            "Authorization":"self.token"
            })
        result = json.loads(resp.data)
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(result['message'], 
            "Invalid token. Please register or login.")
    
    def test_missing_data(self):
        resp = self.client.post('/bucketlists', 
            data=json.dumps({"name":"Go to Canada."}), 
            content_type= "application/json", headers={
            "Authorization":self.token
            })

        result = json.loads(resp.data)
        self.assertEqual(result['error'],
                         "missing data in request.")

    def test_get_all_bucketlists(self):
        """Tests getting the bucketlists."""
        resp = self.client.post('/bucketlists', 
            data=json.dumps(self.bucketlist), 
            content_type= "application/json", headers={
            "Authorization":self.token
            })
        self.assertEqual(resp.status_code, 201)
        response = self.client.get('/bucketlists', headers={
            "Authorization":self.token
            })
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['bucketlists'][0]['name'], 'Go to Canada.')

    def test_no_bucketlists(self):
        """Tests that it returns the message\
         for user with no bucketlists."""    
        response = self.client.get('/bucketlists', headers={
            "Authorization":self.token
            })
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result['message'], 
            'There are no bucketlists for the current user.')

    def test_get_bucketlist_by_id(self):
        """Tests getting a single bucketlist"""
        resp = self.client.post('/bucketlists', 
            data=json.dumps(self.bucketlist), 
            content_type= "application/json", headers={
            "Authorization":self.token
            })
        self.assertEqual(resp.status_code, 201)
        response = self.client.get(
            "/bucketlists/1", headers={
            "Authorization":self.token})
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result["name"], "Go to Canada.")
        self.assertEqual(result["message"], "Bucketlist obtained successfully.")

    def test_get_non_existing_bucketlist(self):    
        resp = self.client.post('/bucketlists', 
            data=json.dumps(self.bucketlist), 
            content_type= "application/json", headers={
            "Authorization":self.token
            })
        self.assertEqual(resp.status_code, 201)
        response = self.client.get(
            "/bucketlists/6", headers={
            "Authorization":self.token})
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data)
        self.assertEqual(result["message"], 
            "Bucketlist with the given id does not exist.")

    def test_delete_bucketlist_by_id(self):
        """Tests deleting a bucketlist."""
        resp = self.client.post('/bucketlists', 
            data=json.dumps(self.bucketlist), 
            content_type= "application/json", headers={
            "Authorization":self.token
            })
        self.assertEqual(resp.status_code, 201)
        response = self.client.get(
            "/bucketlists/1", headers={
            "Authorization":self.token})
        self.assertEqual(response.status_code, 200)
        response = self.client.delete(
            "/bucketlists/1", headers={
            "Authorization":self.token})
        self.assertEqual(response.status_code, 204)   

    def test_update_bucketlist_by_id(self):
        """Tests updating a bucketlist."""
        resp = self.client.post('/bucketlists', 
            data=json.dumps(self.bucketlist), 
            content_type= "application/json", headers={
            "Authorization":self.token
            })
        self.assertEqual(resp.status_code, 201)
        response = self.client.get(
            "/bucketlists/1", headers={
            "Authorization":self.token})
        resp = self.client.put('/bucketlists/1', 
            data=json.dumps({"name":"Go to Canada and visit cousins too."}), 
            content_type= "application/json", headers={
            "Authorization":self.token
            })
        result = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(result["message"], "Bucketlist edited successfully.")
       
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

if __name__ == '__main__':
    unittest.main()
