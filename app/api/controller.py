from flask import jsonify, make_response, request
from flask_httpauth import HTTPTokenAuth
from flask_restful import Resource
from flask.ext.login import current_user, login_required

from .models import BucketList, BucketListItems
from app import db
from .. auth.models import User


class BucketLists(Resource):
    """Shows a list of all bucketlists, and lets you POST to add new bucketlists."""

    def post(self):
        token = request.headers.get('Authorization')
        # import ipdb
        # ipdb.set_trace()
        if token:
            user_id = User.verify_token(token)
            if user_id:
                name = request.json['name']
                description = request.json['description']
                created_by = user_id
                if name is None or description is None:
                    return make_response(
                        jsonify({'data':
                                 {
                                     'message': "Missing data."

                                 }
                                 }), 400)
                bucketlist = BucketList.query.filter_by(name=name).first()
                if bucketlist:
                    return make_response(
                        jsonify({'data':
                                 {
                                     'message': "Bucketlist already created.",
                                     'name': name
                                 }
                                 }), 400)
                else:
                    bucketlist = BucketList(name, description, created_by)
                    db.session.add(bucketlist)
                    db.session.commit()
                    return make_response(
                        jsonify({'data':
                                 {
                                     'message': "Bucketlist created successfully.",
                                     "name": name,
                                     "description": description,
                                     "created_by":created_by

                                 }
                                 }), 201)
            else:
                return make_response(
                    jsonify({'data':
                             {
                                 'message': user_id
                             }
                             }), 401)

    def get(self):
        token = request.headers.get('Authorization')
        if token:
            user_id = User.verify_token(token)
            user_bucketlists = BucketList.query.filter_by(created_by=user_id)
            bucketlists = []
            if user_bucketlists:
                for b_lists in user_bucketlists:
                    bucketlists.append[{
                        "id": b_lists.id,
                        "name": b_lists.name,
                        "description": b_lists.description,
                        "created_by": b_lists.created_by
                    }]
                return make_response(jsonify(BucketLists))

            else:
                return make_response(
                    jsonify({'data':
                             {
                                 'message': "There are no bucketlists for the current user."

                             }
                             }), 404)
        else:
            return make_response(
                jsonify({'data':
                         {
                             'message': "Token verification failed."

                         }
                         }), 401)

    def delete(self):
        token = request.headers.get('Authorization')
        if token:
            user_id = User.verify_token(token)
            user_bucketlists = BucketList.query.filter_by(created_by=user_id)
            if user_bucketlists:
                del_bucketlists = BucketList.delete(created_by=user_id)
                if del_bucketlists:
                    return make_response(jsonify({'data':
                                                  {
                                                      'message': "Bucketlists for current user deleted successful."
                                                  }
                                                  }), 200)
            else:
                return make_response(
                    jsonify({'data':
                             {
                                 'message': "Current user has no bucketlists."

                             }
                             }), 404)
        else:
            return make_response(
                jsonify({'data':
                         {
                             'message': "Token verification failed."

                         }
                         }), 401)


class SingleBucketList(Resource):
    """Shows a single bucketlist item and lets you delete a bucketlist item."""

    def put(self, bucketlist_id):
        token = request.headers.get('Authorization')
        if token:
            user_id = User.verify_token(token)
            bucketlist = Bucketlist.query.filter_by(
                id=bucketlist_id, created_by=user_id).first()
            if not bucketlist:
                return make_response(
                    jsonify({'data':
                             {
                                 'message': "Bucketlist not found."

                             }
                             }), 404)

            new_bucketlist_name = request.json["name"]
            if not new_bucketlist_name:
                return make_response(
                    jsonify({'data':
                             {
                                 'message': "name field is missing."

                             }
                             }), 403)

            if new_bucketlist_name == bucketList.name:
                return make_response(
                    jsonify({'data':
                             {
                                 'message': "Bucketlist name has not been edited ."

                             }
                             }), 403)
            bucketlist.name = new_bucketlist_name
            # bucketlist.date_modified =
            db.session.add(bucketlist)
            db.session.commit()
            return make_response(
                jsonify({'data':
                         {'id': bucketlist.id,
                          'name': bucketlist.name,
                          'date_created': bucketlist.date_created,
                          'date_modified': bucketlist.date_modified,
                          'date_created': bucketlist.created_by,
                          'message': "Bucketlist edited successfully."

                          }
                         }), 200)
        else:
            return make_response(
                jsonify({'data':
                         {
                             'message': "Token verification failed."

                         }
                         }), 401)

    def delete(self, bucketlist_id):
        token = request.headers.get('Authorization')
        if token:
            user_id = User.verify_token(token)
            bucketlist = Bucketlist.query.filter_by(
                id=bucketlist_id, created_by=user_id).first()
            if bucketlist:
                bucketlist = Bucketlist.delete(id=bucketlist_id)
                return make_response(
                    jsonify({'data':
                             {
                                 'message': "Bucketlist deleted successfully.",
                                 'name': bucketlist.name,
                                 "id": bucketlist.id
                             }
                             }), 404)
            else:
                return make_response(
                    jsonify({'data':
                             {
                                 'message': "with given id does not exist."
                             }
                             }), 200)
        else:
            return make_response(
                jsonify({'data':
                         {
                             'message': "Token verification failed."

                         }
                         }), 401)

    def get(self, bucketlist_id):
        token = request.headers.get('Authorization')
        if token:
            user_id = User.verify_token(token)
            bucketlist = BucketList.query.filter_by(id=bucketlist_id).first()
            if bucketlist:
                return make_response(
                    jsonify(
                        {'data':
                         {
                             'name': Bucketlist.name,
                             'description': Bucketlist.description,
                             'message': "with given id does not exist."
                         }
                         }), 200)
            else:
                return make_response(
                    jsonify({'data':
                             {
                                 'message': "Bucketlist with the given id does not exist."
                             }
                             }), 404)
        else:
            return make_response(
                jsonify({'data':
                         {
                             'message': "Token verification failed."

                         }
                         }), 401)


class BucketListItem(Resource):
    """Shows the items on a given bucketlist."""

    def post(self, bucketlist_id):
        token = request.headers.get('Authorization')
        if token:
            user_id = User.verify_token(token)
            data = request.json
            name = data["name"]
            if name:
                item = BucketListItems.query.filter_by(name=name).first()
                if item:
                    return make_response(
                        jsonify({'data':
                                 {
                                     'message': "Item with the given name exists."
                                 }
                                 }), 400)
                b_item = BucketListItems(name, bucketlist_id)
                db.session.add(b_item)
                db.session.commit()
                return make_response(
                    jsonify({'data':
                             {
                                 'message': "Bucket list item added successfully."
                             }
                             }), 200)
            return make_response(
                jsonify({'data':
                         {
                             'message': "name is missing in json string."
                         }
                         }), 400)
        else:
            return make_response(
                jsonify({'data':
                         {
                             'message': "Token verification failed."

                         }
                         }), 401)

    def delete(self, bucketlist_id):
        token = request.headers.get('Authorization')
        if token:
            user_id = User.verify_token(token)
            items = BucketlistItems.delete(bucketlist_id=bucketlist_id)
            if items:
                return make_response(
                    jsonify({'data':
                             {
                                 'message': "Items of the bucketlist deleted successfully.."

                             }
                             }), 200)
            else:
                return make_response(
                    jsonify({'data':
                             {
                                 'message': "No bucketlist items for deletion."

                             }
                             }), 401)

    def get(self, bucketlist_id):
        token = request.headers.get('Authorization')
        if token:
            user_id = User.verify_token(token)
            items = BucketListItems.query.filter_by(
                bucketlist_id=bucketlist_id).all()
            if items:
                item_list = []
                for item in items:
                    item_list.append({
                        "id": item.id,
                        "name": item.name
                    })
                return make_response(
                    jsonify(item_list), 200)
        else:
            return make_response(
                jsonify({'data':
                         {
                             'message': "Token verification failed."

                         }
                         }), 401)


class SingleBucketListItem(Resource):

    def get(self, bucketlist_id, item_id):
        token = request.headers.get('Authorization')
        if token:
            user_id = User.verify_token(token)
            item = BucketListItems.query.filter_by(
                bucketlist_id=bucketlist_id, id=item_id).first()
            if item:
                return make_response(
                    jsonify({'data':
                             {
                                 'message': "Bucketlist item obtained successfully.",
                                 'item_id': item.item_id,
                                 'name': item.name,
                                 'date_created': item.date_created,
                                 'date_modified': item.date_modified


                             }
                             }), 401)

            return make_response(
                jsonify({'data':
                         {
                             'message': "Bucket list item with the id does not exist."

                         }
                         }), 404)
        return make_response(
            jsonify({'data':
                     {
                         'message': "Token verification failed."

                     }
                     }), 401)

    def put(self, bucketlist_id, item_id):
        token = request.headers.get('Authorization')
        if token:
            user_id = User.verify_token(token)
            bucketlistitem = BucketListItem.query.filter_by(
                id=bucketlist_id, item_id=item_id).first()
            if not bucketlistitem:
                return make_response(
                    jsonify({'data':
                             {
                                 'message': "Bucketlist not found."

                             }
                             }), 404)

            new_bucketlistitem_name = request.json["name"]
            if not new_bucketlist_name:
                return make_response(
                    jsonify({'data':
                             {
                                 'message': "name field is missing."

                             }
                             }), 403)

            if new_bucketlistitem_name == bucketlistitem.name:
                return make_response(
                    jsonify({'data':
                             {
                                 'message': "Bucketlistitem name is the same."

                             }
                             }), 403)
            bucketlistitem.name = new_bucketlistitem_name
            # bucketlist.date_modified =
            db.session.add(bucketlistitem)
            db.session.commit()
            return make_response(
                jsonify({'data':
                         {'id': bucketlistitem.id,
                          'name': bucketlistitem.name,
                          'date_created': bucketlistitem.date_created,
                          'date_modified': bucketlistitem.date_modified,
                          'message': "Bucketlist edited successfully."

                          }
                         }), 200)
        else:
            return make_response(
                jsonify({'data':
                         {
                             'message': "Token verification failed."

                         }
                         }), 401)

    def delete(self, bucketlist_id, item_id):
        token = request.headers.get('Authorization')
        if token:
            user_id = User.verify_token(token)
            item = BucketListItems.query.filter_by(
                bucketlist_id=bucketlist_id, id=item_id).first()
            if item:
                db.session.delete(item)
                return make_response(
                    jsonify({'data':
                             {
                                 'message': "Item deleted successfully."

                             }
                             }), 200)
            return make_response(
                jsonify({'data':
                         {
                             'message': "Item doesn't exist."

                         }
                         }), 404)

        return make_response(
            jsonify({'data':
                     {
                         'message': "Token verification failed."

                     }
                     }), 401)
