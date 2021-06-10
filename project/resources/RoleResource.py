from datetime import datetime

from bson import ObjectId
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash

from project import mongo
from flask_jwt_extended import jwt_required, get_jwt_identity

role_arg = reqparse.RequestParser()
role_arg.add_argument('role_name', help='This field cannot be blank', required=True)
role_arg.add_argument('role_description', help='This field cannot be blank', required=True)
# role_arg.add_argument('login_id', help='This field cannot be blank', required=True)
# role_arg.add_argument('org_id', help='This field cannot be blank', required=True)


class CreateRole(Resource):

    @jwt_required()
    def post(self):
        data = role_arg.parse_args()

        if mongo.db.roles_collection.find_one({'role_name': data['role_name']}) is not None:
            return {'message': 'Roll Name /{}/ already exist'.format(data['role_name'])}, 400
        elif mongo.db.users.find_one({'role_description': data['role_description']}) is not None:
            return {'message': 'Role Description /{}/ already exist'.format(data['role_description'])}, 400

        try:
            _id = mongo.db.roles_collection.insert({
                'role_name': data['role_name'],
                'role_description': data['role_description'],
                'created_by': ObjectId(get_jwt_identity()['_id']),
                'created_at': datetime.utcnow()
            })

            return f'{data["role_name"]} is created', 200

        except AttributeError:
            return 'Provide an Name, Username and Password in JSON in request body', 400
