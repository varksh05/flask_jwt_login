from datetime import datetime
from flask_restful import Resource, reqparse
from flask_pymongo import DESCENDING, ASCENDING
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.json_util import ObjectId
from project import mongo

role_arg = reqparse.RequestParser()
role_arg.add_argument('role_name', help='This field cannot be blank', required=True)
role_arg.add_argument('role_description', help='This field cannot be blank', required=True)

role_update = reqparse.RequestParser()
role_update.add_argument('role_name')
role_update.add_argument('role_description')


class CreateRole(Resource):

    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()

            # Check the permission for the role with the current id
            createRolePermission = mongo.db.process_collection.find_one(
                {'_id': ObjectId('60c6e638c19d73a3e81bb76e')}
            )['permission_role_id']

            if current_user['role_id'] in createRolePermission:
                data = role_arg.parse_args()

                if mongo.db.roles_collection.find_one({'role_name': data['role_name']}) is not None:
                    return {'message': 'Role Name /{}/ already exist'.format(data['role_name'])}, 400
                elif mongo.db.users_collection.find_one({'role_description': data['role_description']}) is not None:
                    return {'message': 'Role Description /{}/ already exist'.format(data['role_description'])}, 400

                _id = mongo.db.roles_collection.insert({
                    'role_name': data['role_name'],
                    'role_description': data['role_description'],
                    'created_by': ObjectId(get_jwt_identity()['_id']),
                    'created_at': datetime.utcnow(),
                    'delete_status': False
                })

                print(_id)

                return f'{data["role_name"]} {_id} is created', 200
            return 'Restricted URL', 405

        except AttributeError:
            return 'Provide an Name, Username and Password in JSON in request body', 400


class GetOneRole(Resource):

    @jwt_required()
    def get(self, id):
        try:
            current_user = get_jwt_identity()

            # Check the permission for the role with the current id
            getOneRoleDetailsPermission = mongo.db.process_collection.find_one(
                {'_id': ObjectId('60c6e68cc19d73a3e81bb76f')}
            )['permission_role_id']

            if current_user['role_id'] in getOneRoleDetailsPermission:
                role_data = mongo.db.roles_collection.find_one_or_404({'_id': id, 'delete_status': False})
                response_data = {
                    'role_name': role_data['role_name'],
                    'role_description': role_data['role_description']
                }
                return response_data, 200
            return 'Restricted URL', 405

        except ConnectionRefusedError:
            return 'Provide an Name, Username and Password in JSON in request body', 400


class GetRolesAutoCompleteList(Resource):

    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()

            # Check the permission for the role with the current id
            getRoleAutoCompleteListPermission = mongo.db.process_collection.find_one(
                {'_id': ObjectId('60c6e6eec19d73a3e81bb770')}
            )['permission_role_id']

            
            if current_user['role_id'] in getRoleAutoCompleteListPermission:
                roles_data = mongo.db.roles_collection.find().sort('role_name', ASCENDING)
                response_data = []

                # Formating thhe response data
                for data in roles_data:
                    print(data)
                    response_data.append(data['role_name'])
                return response_data, 200
            return 'Restricted URL', 405

        except KeyError:
            return 'There was a key error', 500


class GetRolesAutoCompleteActiveList(Resource):

    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            
            # Check the permission for the role with the current id
            getRoleAutoCompleteListPermission = mongo.db.process_collection.find_one(
                {'_id': ObjectId('60c6e6eec19d73a3e81bb770')}
            )['permission_role_id']
            
            if current_user['role_id'] in getRoleAutoCompleteListPermission:
                roles_data = mongo.db.roles_collection.find({'delete_status': False}).sort('role_name', ASCENDING)
                response_data = []

                # Formating thhe response data
                for data in roles_data:
                    print(data)
                    response_data.append(data['role_name'])
                return response_data, 200
            return 'Restricted URL', 405

        except KeyError:
            return 'There was a key error', 500


class GetRolesAutoCompleteInactiveList(Resource):

    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            
            # Check the permission for the role with the current id
            getRoleAutoCompleteListPermission = mongo.db.process_collection.find_one(
                {'_id': ObjectId('60c6e6eec19d73a3e81bb770')}
            )['permission_role_id']
            
            if current_user['role_id'] in getRoleAutoCompleteListPermission:
                roles_data = mongo.db.roles_collection.find({'delete_status': True}).sort('role_name', ASCENDING)
                response_data = []

                # Formating thhe response data
                for data in roles_data:
                    print(data)
                    response_data.append(data['role_name'])
                return response_data, 200
            return 'Restricted URL', 405

        except KeyError:
            return 'There was a key error', 500


class GetAllActiveRole(Resource):

    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            
            # Check the permission for the role with the current id
            getAllRoleListPermission = mongo.db.process_collection.find_one(
                {'_id': ObjectId('60c6e71ceb2606d92ef862fd')}
            )['permission_role_id']
            
            if current_user['role_id'] in getAllRoleListPermission:
                roles_data = mongo.db.roles_collection.find({'delete_status': False}).sort('role_name', ASCENDING)
                response_data = []

                # Formating thhe response data
                for data in roles_data:
                    response_data.append({
                        '_id': str(data['_id']),
                        'role_name': data['role_name'],
                        'role_description': data['role_description'],
                    })

                return response_data, 200
            return 'Restricted URL', 405

        except ConnectionRefusedError:
            return 'Provide an Name, Username and Password in JSON in request body', 400


class GetAllInactiveRole(Resource):

    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            
            # Check the permission for the role with the current id
            getAllRoleListPermission = mongo.db.process_collection.find_one(
                {'_id': ObjectId('60c6e71ceb2606d92ef862fd')}
            )['permission_role_id']
            
            if current_user['role_id'] in getAllRoleListPermission:
                roles_data = mongo.db.roles_collection.find({'delete_status': True}).sort('role_name', ASCENDING)
                response_data = []

                # Formating thhe response data
                for data in roles_data:
                    response_data.append({
                        '_id': str(data['_id']),
                        'role_name': data['role_name'],
                        'role_description': data['role_description'],
                    })

                return response_data, 200
            return 'Restricted URL', 405

        except ConnectionRefusedError:
            return 'Provide an Name, Username and Password in JSON in request body', 400


class GetAllRole(Resource):

    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            
            # Check the permission for the role with the current id
            getAllRoleListPermission = mongo.db.process_collection.find_one(
                {'_id': ObjectId('60c6e71ceb2606d92ef862fd')}
            )['permission_role_id']
            
            if current_user['role_id'] in getAllRoleListPermission:
                roles_data = mongo.db.roles_collection.find().sort('role_name', ASCENDING)
                response_data = []

                # Formating thhe response data
                for data in roles_data:
                    response_data.append({
                        '_id': str(data['_id']),
                        'role_name': data['role_name'],
                        'role_description': data['role_description'],
                    })

                return response_data, 200
            return 'Restricted URL', 405

        except ConnectionRefusedError:
            return 'Provide an Name, Username and Password in JSON in request body', 400


class UpdateRole(Resource):

    @jwt_required()
    def put(self, id):
        try:
            req = role_update.parse_args()
            current_user = get_jwt_identity()
            
            # Check the permission for the role with the current id
            updateRolePermission = mongo.db.process_collection.find_one(
                {'_id': ObjectId('60c6e758d2fc6ecdacdf9af4')}
            )['permission_role_id']
            
            if current_user['role_id'] in updateRolePermission:

                # Check the updated Field
                roles_data = mongo.db.roles_collection.find_one_or_404(id)
                if req['role_name'] is not None:
                    roles_data['role_name'] = req['role_name']
                if req['role_description'] is not None:
                    roles_data['role_description'] = req['role_description']

                # Check the updated Field
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

                return f'Updated Successfully! Click to View /role/{id}', 200
            return 'Restricted URL', 405

        except ConnectionRefusedError:
            return 'Provide an Name, Username and Password in JSON in request body', 400


class DeleteRole(Resource):

    @jwt_required()
    def put(self, id):
        try:
            current_user = get_jwt_identity()
            
            # Check the permission for the role with the current id
            deleteRolePermission = mongo.db.process_collection.find_one(
                {'_id': ObjectId('60c6e77f329d5df4fc756789')}
            )['permission_role_id']
            
            if current_user['role_id'] in deleteRolePermission:

                # Find the Role Data based on Role Value and if so the Delete Status is True
                role_data = mongo.db.roles_collection.find_one(id)
                if role_data is None or role_data['delete_status'] is True:
                    return f'Role {id} is not found', 404

                # Check if the Role is used Anywhere
                check_data_use = list(mongo.db.users_collection.find(
                    {'role_id': ObjectId(str(id))}))
                if len(check_data_use) > 0:
                    return f'Data is in User {id}', 403

                # Update the Delete status
                mongo.db.roles_collection.update_one({'_id': id}, {
                    '$set': {
                        'delete_status': True,
                        'modified_by': current_user['_id'],
                        'modified_at': datetime.utcnow()
                    }
                })

                return f'Deleted Successfully! Click to View /roles', 200
            return 'Restricted URL', 405

        except ConnectionRefusedError:
            return 'Provide an Name, Username and Password in JSON in request body', 400

    @jwt_required()
    def delete(self, id):
        try:
            current_user = get_jwt_identity()
            
            # Check the permission for the role with the current id
            removeRolePermission = mongo.db.process_collection.find_one(
                {'_id': ObjectId('60c6e78a329d5df4fc75678a')}
            )['permission_role_id']
            
            if current_user['role_id'] in ['60c2663e00a526d1f07465b3', '60c2666c00a526d1f07465b4']:

                # Find the Role Data based on Role Value
                role_data = mongo.db.roles_collection.find_one(id)
                if role_data is None:
                    return f'Role {id} is not found', 404

                # Check if the Role is used Anywhere
                check_data_use = list(mongo.db.users_collection.find(
                    {'role_id': ObjectId(str(id))}))
                if len(check_data_use) > 0:
                    return f'Data is in User {id}', 403

                # Remove the Data from Collection Permanantely
                mongo.db.roles_collection.delete_one({
                    '_id': id
                })
                return f'Removed Successfully! Click to View /roles', 200
            return 'Restricted URL', 405

        except ConnectionRefusedError:
            return 'Provide an Name, Username and Password in JSON in request body', 400


class ActivateRole(Resource):

    @jwt_required()
    def put(self, id):
        try:
            current_user = get_jwt_identity()

            activateRolePermission = mongo.db.process_collection.find_one(
                {'_id': ObjectId('60c6e797329d5df4fc75678b')}
            )['permission_role_id']
            
            if current_user['role_id'] in activateRolePermission:
                
                # Find the Role Data based on Role Value
                role_data = mongo.db.roles_collection.find_one(id)
                if role_data is None:
                    return f'Role {id} is not found', 404

                # Check the Delete Status if its Deleted or Not
                if role_data['delete_status'] is False:
                    return f'Role {id} is already active', 200

                # Update the Delete Status to True
                mongo.db.roles_collection.update_one({'_id': id}, {
                    '$set': {
                        'delete_status': False,
                        'modified_by': current_user['_id'],
                        'modified_at': datetime.utcnow()
                    }
                })

                return f'Activated Successfully! Click to View /roles', 200
            return 'Restricted URL', 405

        except ConnectionRefusedError:
            return 'Provide an Name, Username and Password in JSON in request body', 400
