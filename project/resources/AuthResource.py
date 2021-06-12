from datetime import datetime

from bson import ObjectId
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash

from project import mongo
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

register_arg = reqparse.RequestParser()
register_arg.add_argument('name', help='This field cannot be blank', required=True)
register_arg.add_argument('username', help='This field cannot be blank', required=True)
register_arg.add_argument('password', help='This field cannot be blank', required=True)
register_arg.add_argument('email', help='This field cannot be blank', required=True)
register_arg.add_argument('dob')
register_arg.add_argument('gender')
register_arg.add_argument('email')
register_arg.add_argument('phone')
register_arg.add_argument('role_id', help='This field cannot be blank', required=True)
register_arg.add_argument('password', help='This field cannot be blank', required=True)

login_arg = reqparse.RequestParser()
login_arg.add_argument('user_id', help='This field cannot be blank', required=True)
login_arg.add_argument('password', help='This field cannot be blank', required=True)

change_password_arg = reqparse.RequestParser()
change_password_arg.add_argument('old_password', help='This field cannot be blank', required=True)
change_password_arg.add_argument('new_password', help='This field cannot be blank', required=True)


class Registration(Resource):
    def post(self):
        data = register_arg.parse_args()

        if mongo.db.users_collection.find_one({'email': data['email']}) is not None:
            return {'message': 'Email {} already exist'.format(data['email'])}, 400
        elif mongo.db.users_collection.find_one({'username': data['username']}) is not None:
            return {'message': 'Username already exist'.format(data['username'])}, 400
        elif mongo.db.users_collection.find_one({'phone': data['phone']}) is not None:
            return {'message': 'Phone already exist'.format(data['phone'])}, 400

        try:
            _id = mongo.db.users_collection.insert({
                'name': data['name'],
                'username': data['username'],
                'password': generate_password_hash(data['password']),
                'dob': data['dob'],
                'gender': data['gender'],
                'email': data['email'],
                'phone': data['phone'],
                'role_id': ObjectId(data['role_id']),
                'created_at': datetime.utcnow()
            })

            # access_token = create_access_token(identity={'_id': str(_id), role_id: str(role_id)})
            # refresh_token = create_refresh_token(identity={'_id': str(_id), role_id: str(role_id)})
            # return {'_id': str(_id), 'access_token': access_token, 'refresh_token': refresh_token}, 200

            return f'{data["name"]} is created', 200

        except AttributeError:
            return 'Provide an Name, Username and Password in JSON in request body', 400


class Login(Resource):
    def post(self):
        data = login_arg.parse_args()

        user_id = data['user_id']
        password = data['password']

        try:
            if mongo.db.users_collection.find_one({'email': user_id}) is None and mongo.db.users_collection.find_one({'username': user_id}) is None and mongo.db.users_collection.find_one({'phone': user_id}) is None:
                return {'message': f'User {user_id} does not exist'}, 404

            if mongo.db.users_collection.find_one({'email': user_id}) is not None:
                _user = mongo.db.users_collection.find_one({'email': user_id})
            elif mongo.db.users_collection.find_one({'username': user_id}) is not None:
                _user = mongo.db.users_collection.find_one({'username': user_id})
            elif mongo.db.users_collection.find_one({'phone': user_id}) is not None:
                _user = mongo.db.users_collection.find_one({'phone': user_id})

            if check_password_hash(pwhash=_user["password"], password=password):
                access_token = create_access_token(
                    identity={'_id': str(_user["_id"]), 'role_id': str(_user["role_id"])},
                    expires_delta=False
                )
                refresh_token = create_refresh_token(
                    identity={'_id': str(_user["_id"]), 'role_id': str(_user["role_id"])},
                    expires_delta=False
                )
                return {
                    '_id': str(_user["_id"]),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, 200

            else:
                return f'Incorrect Password', 404

        except AttributeError:
            return 'Provide an Name, Username and Password in JSON in request body', 400


class ChangePassword(Resource):

    @jwt_required()
    def put(self, id):
        data = change_password_arg.parse_args()
        identity = get_jwt_identity()
        old_password = data['old_password']
        new_password = data['new_password']
        _user = {}

        print(identity)

        try:
            if mongo.db.users_collection.find_one({'_id': id}) is None:
                return 'User id does not exist', 404
            if identity['role_id'] in ['60c2663e00a526d1f07465b3', '60c2666c00a526d1f07465b4'] and identity['role_id'] is str(id):
               
                _user = mongo.db.users_collection.find_one({'_id':  ObjectId(identity["_id"])})
                # Validating the old password to update the new password    
                if check_password_hash(pwhash=_user["password"], password=old_password):
                    mongo.db.users_collection.update_one({
                        '_id': ObjectId(_user['_id'])
                    }, {
                        '$set': {
                            'password': generate_password_hash(new_password),
                        }
                    })
                    return 'Changed Password Successfully', 200
                # Works when the old Password is Incorrect    
                return f'Incorrect Old Password', 401
            return f'User does not have authority to change password for {_user["username"]}', 401

        except AttributeError:
            return 'Provide an Name, Username and Password in JSON in request body', 400

