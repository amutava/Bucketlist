from flask import jsonify, abort, make_response, url_for
from flask_httpauth import HTTPTokenAuth

from models import BucketList


auth = HTTPTokenAuth('Bearer')


	@api.route('/bucketlists/', methods=['POST'])
	def create_bucketlist():
		pass

	@api.route('/bucketlists/<int:id>', methods=['PUT'])
	def update_bucketlist():
		pass

	@api.route('/bucketlists/<int:id>', methods=['DELETE'])
	def delete_bucketlist():
		pass

	@api.route('/bucketlists/', methods=['GET'])
	def get_bucketlists():
		pass

	@api.route('/bucketlist/<int:id>', methods='GET')
	def get_bucketlist():
		pass
   

   @auth.error_handler
	def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    	return make_response(jsonify({'error': 'Unauthorized access'}), 403)


	@app.errorhandler(400)
	def bad_request(error):
    	return make_response(jsonify({'error': 'Bad request'}), 400)


	@app.errorhandler(404)
	def not_found(error):
    	return make_response(jsonify({'error': 'Not found'}), 404)
