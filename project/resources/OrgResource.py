from datetime import datetime

from bson import ObjectId
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash

from project import mongo
from flask_jwt_extended import jwt_required, get_jwt_identity

org_arg = reqparse.RequestParser()
org_arg.add_argument('org_name', help='This field cannot be blank', required=True)
org_arg.add_argument('org_description', help='This field cannot be blank', required=True)

class CreateOrg(Resource):

    @jwt_required()
    def post(self):
        data = org_arg.parse_args()

        try:
            if mongo.db.orgs_collection.find_one({'org_name': data['org_name']}) is not None:
                return {'message': 'Organisation Name /{}/ already exist'.format(data['org_name'])}, 400
            elif mongo.db.users.find_one({'org_description': data['org_description']}) is not None:
                return {'message': 'Organisation Description /{}/ already exist'.format(data['org_description'])}, 400

            _id = mongo.db.orgs_collection.insert({
                'org_name': data['org_name'],
                'org_description': data['org_description'],
                'created_by': ObjectId(get_jwt_identity()['_id']),
                'created_at': datetime.utcnow()
            })

            return f'{data["org_name"]} is created', 200

        except AttributeError:
            return 'Provide an Name, Username and Password in JSON in request body', 400
