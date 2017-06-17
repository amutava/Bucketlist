from flask import jsonify, make_response, request
from flask_httpauth import HTTPTokenAuth
from flask_restful import Resource
from flask_login import current_user, login_required

from application.api.models import BucketList, BucketListItems
from application import db
from .. auth.models import User


class BucketLists(Resource):
    """Shows a list of all bucketlists, and lets you POST to add new bucketlists."""

    def post(self):
        try:
            token = request.headers.get('Authorization')
            if token:
                user_id = User.verify_token(token)
                if isinstance(user_id, int):
                    name = request.json['name']
                    description = request.json['description']
                    created_by = user_id
                    if not name:
                        return make_response(
                            jsonify(
                                {
                                    'message': " Missing name."
                                }
                            ), 400)
                    if not description:
                        return make_response(
                            jsonify(
                                {
                                    'message': "Missing password."
                                }
                            ), 400)
                    bucketlist = BucketList.query.filter_by(name=name).\
                        first()
                    if bucketlist:
                        return make_response(
                            jsonify(
                                {
                                    'message': "Bucketlist already created.",
                                    'name': name
                                }
                            ), 201)
                    else:
                        bucketlist = BucketList(name, description, created_by)
                        db.session.add(bucketlist)
                        db.session.commit()
                        return make_response(
                            jsonify(
                                {
                                    'message': "Bucketlist created successfully.",
                                    "name": name,
                                    "description": description,
                                    "created_by": created_by
                                }
                            ), 201)
                else:
                    return make_response(
                        jsonify(
                            {
                                'message': user_id
                            }
                        ), 401)
        except:
            return make_response(jsonify({
                "error": "missing data in request."
            }), 404)

    def get(self):
        token = request.headers.get('Authorization')
        user_id = User.verify_token(token)
        if isinstance(user_id, int):
            limit = int(request.args.get("limit", 20))
            page = int(request.args.get("page", 1))
            if int(limit) > 100:
                limit = 100
            search = request.args.get('q', None)
            if search:
                user_bucketlists = BucketList.query.filter(
                    BucketList.name.ilike('%' + search + '%')).filter_by(user_id=user.id)
                if not bucketlists_query.count():
                    return {"message":
                        "No bucketlists found matching '{}'".format(search)}
            else:
                user_bucketlists = BucketList.query.filter_by(
                created_by=user_id)
            paginated_bucketlists = user_bucketlists.paginate(page=page,
                                                 per_page=limit,
                                                 error_out=False)
            if paginated_bucketlists:
                bucketlists = []
                for b_lists in paginated_bucketlists.items:
                        bucketlists.append({
                        "id": b_lists.id,
                        "name": b_lists.name,
                        "description": b_lists.description,
                        "created_by": b_lists.created_by
                        })
                return make_response(jsonify({'bucketlists': bucketlists
                                             }), 200)
            else:
                    return make_response(
                    jsonify(
                        {
                            'message': "There are no bucketlists for the current user."
                        }
                    ), 404)

        else:
            return make_response(
                jsonify(
                    {
                        'message': user_id
                    }
                ), 401)


class SingleBucketList(Resource):
    """Shows a single bucketlist item and lets you delete a bucketlist item."""

    def put(self, bucketlist_id):
        token = request.headers.get('Authorization')
        user_id = User.verify_token(token)
        if isinstance(user_id, int):
            bucketlist = BucketList.query.filter_by(
                created_by=user_id, id=bucketlist_id).first()
            if not bucketlist:
                return make_response(
                    jsonify(
                        {
                            'message': "Bucketlist not found."
                        }
                    ), 404)
            new_bucketlist_name = request.json["name"]
            if not new_bucketlist_name:
                return make_response(
                    jsonify(
                        {
                            'message': "name field is missing."

                        }
                    ), 400)
            if new_bucketlist_name == bucketlist.name:
                return make_response(
                    jsonify(
                        {
                            'message': "Bucketlist name is the same as before ."
                        }
                    ), 403)
            bucketlist.name = new_bucketlist_name
            db.session.add(bucketlist)
            db.session.commit()
            return make_response(
                jsonify(
                    {'id': bucketlist.id,
                     'name': bucketlist.name,
                     'date_created': bucketlist.date_created,
                     'date_modified': bucketlist.date_modified,
                     'date_created': bucketlist.created_by,
                     'description': bucketlist.description,
                     'message': "Bucketlist edited successfully."
                     }
                ), 200)
        else:
            return make_response(
                jsonify(
                    {
                        'message': user_id
                    }
                ), 401)

    def delete(self, bucketlist_id):
        token = request.headers.get('Authorization')
        user_id = User.verify_token(token)
        if isinstance(user_id, int):
            bucketlist = BucketList.query.filter_by(
                id=bucketlist_id, created_by=user_id).first()
            if bucketlist:
                db.session.delete(bucketlist)
                db.session.commit()
                return make_response(
                    jsonify(
                        {
                            'message': "Bucketlist deleted successfully."
                        }
                    ), 204)
            else:
                return make_response(
                    jsonify(
                        {
                            'message': "Bucketlist with given id does not exist."
                        }
                    ), 200)
        else:
            return make_response(
                jsonify({
                    'message': user_id
                }
                ), 404)

    def get(self, bucketlist_id):
        token = request.headers.get('Authorization')
        user_id = User.verify_token(token)
        if isinstance(user_id, int):
            bucketlist = BucketList.query.filter_by(id=bucketlist_id).first()
            item = BucketListItems.query.filter_by(
                bucketlist_id=bucketlist_id).all()
            if bucketlist:
                items = []
                if item:
                    for b_item in item:
                        items.append({"name": b_item.name,
                                      "id": b_item.id,
                                      "date_created": b_item.date_created,
                                      "date_modified": b_item.date_modified,
                                      "done": b_item.done})
                    return make_response(
                        jsonify(
                            {'id': bucketlist.id,
                                'name': bucketlist.name,
                                'description': bucketlist.description,
                                'items': items,
                                'message': "Bucketlist obtained successfully.",
                                'created_by': bucketlist.created_by,
                                'date_created': bucketlist.date_created
                             }
                        ), 200)
                return make_response(
                    jsonify(
                        {'id': bucketlist.id,
                            'name': bucketlist.name,
                            'description': bucketlist.description,
                            'items': items,
                            'message': "Bucketlist obtained successfully.",
                            'created_by': bucketlist.created_by,
                            'date_created': bucketlist.date_created
                         }
                    ), 200)
            else:
                return make_response(
                    jsonify(
                        {
                            'message': "Bucketlist with the given id does not exist."
                        }
                    ), 404)
        else:
            return make_response(
                jsonify(
                    {
                        'message': user_id
                    }
                ), 401)


class BucketListItem(Resource):
    """Shows the items on a given bucketlist."""

    def post(self, bucketlist_id):
        try:
            token = request.headers.get('Authorization')
            user_id = User.verify_token(token)
            if isinstance(user_id, int):
                name = request.json["name"]
                if name:
                    item = BucketListItems.query.filter_by(
                        name=name, bucketlist_id=bucketlist_id).first()
                    if item:
                        return make_response(
                            jsonify(
                                {
                                    'message': "Item with the given name exists.",
                                    'name': name
                                }
                            ), 409)
                    b_item = BucketListItems(name, bucketlist_id)
                    db.session.add(b_item)
                    db.session.commit()
                    return make_response(
                        jsonify(
                            {
                                'message': "Bucket list item added successfully.",
                                'name': name
                            }
                        ), 200)
                return make_response(
                    jsonify(
                        {
                            'message': "name is missing in json string."
                        }
                    ), 400)
            else:
                return make_response(
                    jsonify(
                        {
                            'message': user_id
                        }
                    ), 401)
        except:
            return make_response(jsonify({
                "error": "missing data in request."
            }), 404)

    def get(self, bucketlist_id):
        token = request.headers.get('Authorization')
        user_id = User.verify_token(token)
        if isinstance(user_id, int):
            items = BucketListItems.query.filter_by(
                bucketlist_id=bucketlist_id).all()
            if items:
                item_list = []
                for item in items:
                    item_list.append({
                        "id": item.id,
                        "name": item.name,
                        "message": "Bucketlist item obtained successfully.",
                        "date_created": item.date_created,
                        "done": item.done
                    })
                return make_response(
                    jsonify({"Bucketlistitems":

                             item_list}), 200)
        else:
            return make_response(
                jsonify(
                    {
                        'message': user_id
                    }
                ), 401)


class SingleBucketListItem(Resource):

    def get(self, bucketlist_id, item_id):
        token = request.headers.get('Authorization')
        user_id = User.verify_token(token)
        if isinstance(user_id, int):
            item = BucketListItems.query.filter_by(
                bucketlist_id=bucketlist_id, id=item_id).first()
            if item:
                return make_response(
                    jsonify(
                        {
                            'message': "Bucketlist item obtained successfully.",
                            'item_id': item.id,
                            'name': item.name,
                            'date_created': item.date_created,
                            'date_modified': item.date_modified
                        }
                    ), 200)
            return make_response(
                jsonify(
                    {
                        'message': "Bucket list item with the id does not exist."
                    }
                ), 404)
        return make_response(
            jsonify(
                {
                    'message': user_id
                }
            ), 401)

    def put(self, bucketlist_id, item_id):
        token = request.headers.get('Authorization')
        user_id = User.verify_token(token)
        if isinstance(user_id, int):
            bucketlistitem = BucketListItems.query.filter_by(
                bucketlist_id=bucketlist_id, id=item_id).first()
            if not bucketlistitem:
                return make_response(
                    jsonify(
                        {
                            'message': "Bucketlist item not found."
                        }
                    ), 404)

            new_bucketlistitem_name = request.json["name"]
            if not new_bucketlistitem_name:
                return make_response(
                    jsonify(
                        {
                            'message': "name field is missing."
                        }
                    ), 400)
            if new_bucketlistitem_name == bucketlistitem.name:
                return make_response(
                    jsonify(
                        {
                            'message': "Bucketlistitem name is the same."
                        }
                    ), 403)
            bucketlistitem.name = new_bucketlistitem_name
            db.session.add(bucketlistitem)
            db.session.commit()
            return make_response(
                jsonify(
                    {'id': bucketlistitem.id,
                     'name': bucketlistitem.name,
                     'date_created': bucketlistitem.date_created,
                     'date_modified': bucketlistitem.date_modified,
                     'message': "Bucketlist edited successfully."
                     }
                ), 201)
        else:
            return make_response(
                jsonify(
                    {
                        'message': user_id
                    }
                ), 401)

    def delete(self, bucketlist_id, item_id):
        token = request.headers.get('Authorization')
        user_id = User.verify_token(token)
        if isinstance(user_id, int):
            item = BucketListItems.query.filter_by(
                bucketlist_id=bucketlist_id, id=item_id).first()
            if item:
                db.session.delete(item)
                return make_response(
                    jsonify(
                        {
                            'message': "Item deleted successfully.",
                            'name': item.name,
                            'date_created': item.date_created
                        }
                    ), 204)
            return make_response(
                jsonify(
                    {
                        'message': "Item doesn't exist."
                    }
                ), 404)

        return make_response(
            jsonify(
                {
                    'message': user_id
                }
            ), 401)
