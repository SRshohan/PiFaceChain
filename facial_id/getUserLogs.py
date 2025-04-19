from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from command import QueryFromBlockchain
import json

class UserLogs(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('campusID')
        if not email:
            return jsonify({'error': 'No email provided'})
        # query blockchain database
        try:
            ot = QueryFromBlockchain("GetAssetHistory", [email])
            if ot["success"]:
                payload = eval(ot["output"])
                return jsonify({'message': 'User logs retrieved successfully', 'logs': payload})
            else:
                return jsonify({'error': 'Failed to retrieve user logs'})
        except Exception as e:
            return jsonify({'error': str(e)})
        

app = Flask(__name__)
api = Api(app)
CORS(app)
api.add_resource(UserLogs, '/getUserLogs')
if __name__ == '__main__':
    app.run(debug=True)
            