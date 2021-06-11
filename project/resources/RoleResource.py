from datetime import datetime

from bson.json_util import ObjectId, dumps
from flask import jsonify
from flask_pymongo import PyMongo
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash

from project import mongo
from flask_jwt_extended import jwt_required, get_jwt_identity

role_arg = reqparse.RequestParser()
role_arg.add_argument('role_name', help='This field cannot be blank', required=True)
role_arg.add_argument('role_description', help='This field cannot be blank', required=True)

role_update = reqparse.RequestParser()
role_arg.add_argument('role_name')
role_arg.add_argument('role_description')

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
                'delete_status': 0,
                'created_at': datetime.utcnow()
            })

            return f'{data["role_name"]} is created', 200

        except AttributeError:
            return 'Provide an Name, Username and Password in JSON in request body', 400


class GetOneRole(Resource):

    @jwt_required()
    def get(self, id):
        try:
            current_user = get_jwt_identity()
            if current_user['role_id'] in ['60c2663e00a526d1f07465b3', '60c2666c00a526d1f07465b4']:
                role_data = mongo.db.roles_collection.find_one_or_404(id)
                response_data = {
                    'role_name': role_data['role_name'],
                    'role_description': role_data['role_description']
                }
                return response_data, 200
            return 'Restricted URL', 401

        except ConnectionRefusedError:
            return 'Provide an Name, Username and Password in JSON in request body', 400


class GetRolesAutoCompleteList(Resource):

    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            if current_user['role_id'] in ['60c2663e00a526d1f07465b3', '60c2666c00a526d1f07465b4']:
                roles_data = mongo.db.roles_collection.find()
                response_data = []
                for data in roles_data:
                    print(data)
                    response_data.append(data['role_name'])
                return response_data, 200
            return 'Restricted URL', 401

        except ConnectionRefusedError:
            return 'Provide an Name, Username and Password in JSON in request body', 400



class GetAllRole(Resource):

    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            if current_user['role_id'] in ['60c2663e00a526d1f07465b3', '60c2666c00a526d1f07465b4']:
                roles_data = mongo.db.roles_collection.find()
                response_data = []
                for data in roles_data:
                    print(data)
                    response_data.append({
                        'role_name': data['role_name'],
                        'role_description': data['role_description']
                    })
                return response_data, 200
            return 'Restricted URL', 401

        except ConnectionRefusedError:
            return 'Provide an Name, Username and Password in JSON in request body', 400


class UpdateRole(Resource):

    @jwt_required()
    def put(self, id):
        try:
            req = role_update.parse_args()
            current_user = get_jwt_identity()
            if current_user['role_id'] in ['60c2663e00a526d1f07465b3', '60c2666c00a526d1f07465b4']:
                roles_data = mongo.db.roles_collection.find_one_or_404(id)
                if req['role_id'] is not None:
                    roles_data['role_id'] =  req['role_id']
                if req['role_description'] is not None:
                    roles_data['role_description'] = req['role_description']
                response_data = []
                mongo.db.roles_collection.update_one({
                    '_id': id
                }, {
                    '$set': {
                        'role_name': roles_data['role_name'],
                        'role_description': roles_data['role_description'],
                        'modified_by': current_user['_id'],
                        'modified_at': datetime.utcnow()
                    }
                })

                return f'Deleted Successfully! Click to View /role/{id}', 200
            return 'Restricted URL', 401

        except ConnectionRefusedError:
            return 'Provide an Name, Username and Password in JSON in request body', 400


class DeleteRole(Resource):

    @jwt_required()
    def put(self, id):
        try:
            current_user = get_jwt_identity()
            if current_user['role_id'] in ['60c2663e00a526d1f07465b3', '60c2666c00a526d1f07465b4']:
                role_data = mongo.db.roles_collection.find_one(id)
                if role_data is not None:
                    mongo.db.roles_collection.update_one({
                        '_id': id
                    }, {
                        '$set': {
                            'delete_status': 1,
                            'modified_by': current_user['_id'],
                            'modified_at': datetime.utcnow()
                        }
                    })
                    return f'Deleted Successfully! Click to View /roles', 200
                return f'User {id} is not found', 404
            return 'Restricted URL', 401

        except ConnectionRefusedError:
            return 'Provide an Name, Username and Password in JSON in request body', 400


class RemoveRole(Resource):

    @jwt_required()
    def delete(self, id):
        try:
            current_user = get_jwt_identity()
            if current_user['role_id'] in ['60c2663e00a526d1f07465b3', '60c2666c00a526d1f07465b4']:
                role_data = mongo.db.roles_collection.find_one(id)
                if role_data is not None:
                    mongo.db.roles_collection.delete_one({
                        '_id': id
                    })
                    return f'Removed Successfully! Click to View /roles', 200
                return f'User {id} is not found', 404
            return 'Restricted URL', 401

        except ConnectionRefusedError:
            return 'Provide an Name, Username and Password in JSON in request body', 400