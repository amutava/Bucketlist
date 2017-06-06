import os
import unittest
import json

from flask import Flask
from flask_httpauth import HTTPTokenAuth

from .. auth.models import db, User
from app import create_app, db


class BucketListTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.ctx = self.app.app_context()
        self.client = self.app.test_client()
        self.ctx.push()
        db.drop_all()
        db.create_all()
        self.bucketlist = {'name': 'Go to Canada.'}

    def test_create_bucketlist(self):
        resp = self.client.post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Go to Canada', str(resp.data))

    def test_get_bucketlists(self):
        resp = self.client.post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)
        resp = self.client.get('/bucketlists/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Go to Canada', str(resp.data))

    def test_get_bucketlist_by_id(self):
        resp = self.client.post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)
        result_in_json = json.loads(
            resp.data.decode('utf-8').replace("'", "\""))
        result = self.client.get(
            "/bucketlists/{}".format(result_in_json["id"]))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to Canada', str(result.data))

    def test_delete_bucketlist(self):
        resp = self.client.post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)
        rv = self.client.delete('/bucketlists/1')
        self.assertEqual(rv.status_code, 200)
        result = self.client.get('/bucketlists/1')
        self.assertEqual(result.status_code, 404)

    def test_update_bucketlist(self):
        resp = self.client.post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)
        rv = self.client.put('/bucketlists/1',
                               data={"name", "Don't just go to canada but meet your cousins."})
        self.assertEqual(rv.status_code, 200)
        result = self.client.get('/bucketlists/1')
        self.assertIn("Don't just go to canada", str(result.data))

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

if __name__ == '__main__':
    unittest.main()
