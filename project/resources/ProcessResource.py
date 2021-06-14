from datetime import datetime
from flask_pymongo import ASCENDING
from bson import ObjectId
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash

from project import mongo
from flask_jwt_extended import jwt_required, get_jwt_identity


process_arg = reqparse.RequestParser()
process_arg.add_argument('process_name', help='This field cannot be blank', required=True)
process_arg.add_argument('process_description', help='This field cannot be blank', required=True)
process_arg.add_argument('permission_role_id', action='append')


class CreateProcess(Resource):
    
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()

            # Check the permission for the process with the current id
            createProcessPermission = mongo.db.process_collection.find_one(
                {'_id': ObjectId('60c58bbe91a4288e101faabf')}
            )['permission_role_id']

            if current_user['role_id'] in createProcessPermission:
                data = process_arg.parse_args()

                if mongo.db.process_collection.find_one({'process_name': data['process_name']}) is not None:
                    return {'message': 'Process Name /{}/ already exist'.format(data['process_name'])}, 400
                elif mongo.db.users_collection.find_one({'process_description': data['process_description']}) is not None:
                    return {'message': 'Process Description /{}/ already exist'.format(data['process_description'])}, 400

                _id = mongo.db.process_collection.insert({
                    'process_name': data['process_name'],
                    'process_description': data['process_description'],
                    'permission_role_id': data['permission_role_id'],
                    'created_by': ObjectId(get_jwt_identity()['_id']),
                    'created_at': datetime.utcnow(),
                    'delete_status': False
                })

                return f'{data["process_name"]} is created', 200
            return 'Restricted URL', 405

        except AttributeError:
            return 'Provide an Name, Username and Password in JSON in request body', 400

class GetOneProcess(Resource):
    
    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            
            # Check the permission for the process with the current id
            getOneProcessDetails = mongo.db.process_collection.find_one(
                {'_id': ObjectId('60c590ae91a4288e101faac3')}
            )['permission_role_id']
            
            print(getOneProcessDetails)
            
            if current_user['role_id'] in getOneProcessDetails:
                process_data = mongo.db.process_collection.find_one_or_404({'_id': id, 'delete_status': False})
                response_data = {
                    'process_name': process_data['process_name'],
                    'process_description': process_data['process_description'],
                    'permission_role_id': process_data['permission_role_id']
                }
                return response_data, 200
            return 'Restricted URL', 405

        except ConnectionRefusedError:
            return 'Provide an Name, Username and Password in JSON in request body', 400


class GetAllProcesses(Resource):
    
    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            
            # Check the permission for the process with the current id
            getAllProcessesDetails = mongo.db.process_collection.find_one(
                {'_id': ObjectId('60c6efe3046458e787da9260')}
            )['permission_role_id']

            if current_user['role_id'] in getAllProcessesDetails:
                processes_data = mongo.db.process_collection.find({'delete_status': False}).sort('process_name', ASCENDING)
                response_data = []

                # Formating thhe response data
                for data in processes_data:
                    response_data.append({
                        'process_name': data['process_name'],
                        'process_description': data['process_description'],
                        'permission_role_id': data['permission_role_id']
                    })

                return response_data, 200
            return 'Restricted URL', 405

        except ConnectionRefusedError:
            return 'Provide an Name, Username and Password in JSON in request body', 400
