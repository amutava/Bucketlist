from flask import jsonify, abort, make_response, url_for
from flask_httpauth import HTTPTokenAuth
from flask_restful import Resource

from .models import BucketList
from app import db
from .. auth.models import User



class BucketLists(Resource):
    """Shows a list of all bucketlists, and lets you POST to add new bucketlists."""
    def post(self):
        name = request.json.get('name')
        description = request.json.get('description')
        created_by = User.id
        if name is None or description is None:
            abort(400, {
                "error": {
                    "message": "Missing data."
                }
            })
        bucketlist = BucketList.query.filter_by(name=name).first()
        if bucketlist:
            abort(400, {
                "error": {
                    "message": "Bucketlist already created."
                }
            })
        else:
            bucketlist = BucketList(name, description, created_by)
            db.session.add(bucketlist)
            db.session.commit()
            return jsonify({
                "message": "Bucketlist added successfully."
            }), 201

    def get(self):
        bucketlists = BucketList.query.filter_by(
            created_by=User.id)
        if bucketlists:
            for bucketlist in bucketlists:
                return jsonify({"name": bucketlist.name,
                               "id": bucketlist.id})
        else:
            abort(404, {
                "error": {
                    "message": "No bucketlists for the current user."
                }
            })

    def delete(self):
        pass        

class SingleBucketList(Resource):
    """Shows a single bucketlist item and lets you delete a bucketlist item."""
    
    def put(self, bucketlist_id):
        pass

    def delete(self, bucketlist_id):
        bucketlist = Bucketlist.query.filter_by(id=bucketlist_id).first()
        if bucketlist:
            bucketlist = Bucketlist.delete(id=bucketlist_id)
            return jsonify({"message": "Bucketlist deleted successfully.",
                           "name": bucketlist.name,
                           "id": bucketlist.id})
        else:
            abort(404, {
                "error": {
                    "message": "Bucketlist with the given id doesn't exist."
                }
            })
    
    def get(self, bucketlist_id):
        bucketlist = BucketList.query.filter_by(id=bucketlist_id).first()
        if bucketlist:
            return jsonify({"name": bucketlist.name,
                           "desciption": bucketlist.desciption,
                           "message": "Bucketlist obtained successfully."})
        else:
            abort(404, {
                "error": {
                    "message": "Bucketlist with the given id doesn't exist."
                }
            })
    
class BucketListItem(Resource):
    """Shows the items on a given bucketlist."""
    
    def delete(self, bucketlist_id):
        pass

    
    def put(self, bucketlist_id):
        pass

    def get(self, bucketlist_id):
        pass    

    # @auth.error_handler
    # def unauthorized(self):
    #     # return 403 instead of 401 to prevent browsers from displaying the default
    #     # auth dialog
    #     return make_response(jsonify({'error': 'Unauthorized access'}), 403)

    # @app.errorhandler(400)
    # def bad_request(self, error):
    #     return make_response(jsonify({'error': 'Bad request'}), 400)

    # @app.errorhandler(404)
    # def not_found(self, error):
    #     return make_response(jsonify({'error': 'Not found'}), 404)
