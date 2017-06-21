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
        self.user = {
            "username": "angie",
            "password": "angie"
        }
        self.added_user = User(self.user["username"],
                               self.user["password"])
        db.session.add(self.added_user)
        db.session.commit()
        user = User.query.filter_by(username='angie').first()
        self.bucketlist = {
            'name': 'Go to Canada.',
            'description': "with an helicopter."
        }
        self.token = user.generate_auth_token(user.id)

    def test_create_bucketlist_item(self):
        """Tests adding a bucketlist item."""
        resp = self.client.post('/bucketlists',
                                data=json.dumps(self.bucketlist),
                                content_type="application/json", headers={
                                    "Authorization": self.token
                                })
        self.assertEqual(resp.status_code, 201)
        response = self.client.get(
            "/bucketlists/1", headers={
                "Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        resp_item = self.client.post('/bucketlistitems/1/items',
                                     data=json.dumps(
                                         {"name": "visit the busy surburbs."}),
                                     content_type="application/json", headers={
                                         "Authorization": self.token
                                     })
        result = json.loads(resp_item.data)
        self.assertEqual(result["message"],
                         "Bucket list item added successfully.")
        self.assertEqual(resp.status_code, 201)

    def test_duplicate_bucketlist_item(self):
        """Tests adding an item with a duplicate name."""
        resp = self.client.post('/bucketlists',
                                data=json.dumps(self.bucketlist),
                                content_type="application/json", headers={
                                    "Authorization": self.token
                                })
        self.assertEqual(resp.status_code, 201)
        resp_item = self.client.post('/bucketlistitems/1/items',
                                     data=json.dumps(
                                         {"name": "visit the busy surburbs."}),
                                     content_type="application/json", headers={
                                         "Authorization": self.token
                                     })
        self.assertEqual(resp.status_code, 201)
        resp_item2 = self.client.post('/bucketlistitems/1/items',
                                      data=json.dumps(
                                          {"name": "visit the busy surburbs."}),
                                      content_type="application/json", headers={
                                          "Authorization": self.token
                                      })
        result = json.loads(resp_item2.data)
        self.assertEqual(result["message"], "Item with the given name exists.")
        self.assertEqual(resp_item2.status_code, 409)

    def test_get_bucketlist_items(self):
        """Tests getting bucketlist items."""
        resp = self.client.post('/bucketlists',
                                data=json.dumps(self.bucketlist),
                                content_type="application/json", headers={
                                    "Authorization": self.token
                                })
        self.assertEqual(resp.status_code, 201)

        resp_item = self.client.post('/bucketlistitems/1/items',
                                     data=json.dumps(
                                         {"name": "visit the busy surburbs."}),
                                     content_type="application/json", headers={
                                         "Authorization": self.token
                                     })

        self.assertEqual(resp_item.status_code, 200)
        resp_item = self.client.get('/bucketlistitems/1/items', headers={
            "Authorization": self.token
        })
        self.assertEqual(resp_item.status_code, 200)

    def test_get_bucketlist_item_id(self):
        """Gets a bucketlist item by id."""
        resp = self.client.post('/bucketlists',
                                data=json.dumps(self.bucketlist),
                                content_type="application/json", headers={
                                    "Authorization": self.token
                                })
        self.assertEqual(resp.status_code, 201)
        resp_item = self.client.post('/bucketlistitems/1/items',
                                     data=json.dumps(
                                         {"name": "visit the busy surburbs."}),
                                     content_type="application/json", headers={
                                         "Authorization": self.token
                                     })
        self.assertEqual(resp.status_code, 201)
        get_item = self.client.get('/bucketlistitems/1/items/1', headers={
            "Authorization": self.token
        })
        self.assertEqual(resp.status_code, 201)

    def test_update_busketlistitem_by_id(self):
        """Tests updating a bucketlist by id."""
        resp = self.client.post('/bucketlists',
                                data=json.dumps(self.bucketlist),
                                content_type="application/json", headers={
                                    "Authorization": self.token
                                })
        self.assertEqual(resp.status_code, 201)
        resp_item = self.client.post('/bucketlistitems/1/items',
                                     data=json.dumps(
                                         {"name": "visit the busy surburbs."}),
                                     content_type="application/json", headers={
                                         "Authorization": self.token
                                     })
        self.assertEqual(resp.status_code, 201)
        update_item = self.client.put('/bucketlistitems/1/items/1',
                                      data=json.dumps(
                                          {"name": "visit the busy surburbs and museums too."}),
                                      content_type="application/json", headers={
                                          "Authorization": self.token
                                      })
        self.assertEqual(update_item.status_code, 201)

    def test_delete_bucketlistitem_by_id(self):
        """Tests deleting a bucketlist by id."""
        resp = self.client.post('/bucketlists',
                                data=json.dumps(self.bucketlist),
                                content_type="application/json", headers={
                                    "Authorization": self.token
                                })
        self.assertEqual(resp.status_code, 201)
        resp_item = self.client.post('/bucketlistitems/1/items',
                                     data=json.dumps(
                                         {"name": "visit the busy surburbs."}),
                                     content_type="application/json", headers={
                                         "Authorization": self.token
                                     })
        self.assertEqual(resp.status_code, 201)
        delete_item = self.client.delete('/bucketlistitems/1/items/1',
                                         headers={
                                             "Authorization": self.token
                                         })
        self.assertEqual(delete_item.status_code, 204)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

if __name__ == '__main__':
    unittest.main()
