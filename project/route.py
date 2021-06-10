from project import app, mongo, jwt
from flask import jsonify, request
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from bson.json_util import dumps, ObjectId
from flask_jwt_extended import (
    jwt_required,
    create_access_token, create_refresh_token,
    get_jwt_identity
)


@app.route('/', methods=['GET'])
def home():
    message = {
        'project-name': 'flask-extended',
        'message': 'Welcome to ' + request.url,
        'author': 'Valliyappan S'
    }

    resp = jsonify(message)
    resp.status_code = 200
    return resp


@app.route('/register', methods=['POST'])
def register():
    try:
        name = request.json.get('name', None)
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        dob = request.json.get('dob', None)
        gender = request.json.get('gender', None)
        email = request.json.get('email', None)
        phone = request.json.get('phone', None)
        role_id = request.json.get('role', None)

        if not name:
            return 'Name is Required', 400
        if not username:
            return 'Username is Required', 400
        if not password:
            return 'Password is Required', 400
        if not email:
            return 'Email is Required', 400
        if not phone:
            return 'Phone is Required', 400
        if not role_id:
            return 'Role is Required', 400
        if mongo.db.users.find_one({'email': email}) is not None:
            return 'User Email already exists', 400
        if mongo.db.users.find_one({'username': username}) is not None:
            return 'Username already exists', 400
        if mongo.db.users.find_one({'phone': phone}) is not None:
            return 'Phone already exists', 400

        _hashed_password = generate_password_hash(password)
        _id = mongo.db.users.insert({
            'name': name,
            'username': username,
            'password': _hashed_password,
            'dob': dob,
            'gender': gender,
            'email': email,
            'phone': phone,
            'role_id': ObjectId(role_id),
            'created_at': datetime.utcnow()
        })

        access_token = create_access_token(identity={'_id': str(_id), role_id: str(role_id)})
        refresh_token = create_refresh_token(identity={'_id': str(_id), role_id: str(role_id)})
        return {'_id': str(_id), 'access_token': access_token, 'refresh_token':  refresh_token}, 200

    except AttributeError:
        return 'Provide an Name, Username and Password in JSON in request body', 400


@app.route('/roles', methods=['GET'])
@jwt_required()
def get_all_role():
    user = get_jwt_identity()
    if mongo.db.roles.find_one({'_id': ObjectId(user["role_id"])})["code"] in ('ADMIN', 'SUPER_ADMIN', 'MEMBER_ADMIN'):
        return dumps(mongo.db.roles.find())
    return {'message': 'You don\'t have access to this data'}, 401


@app.route('/role/create', methods=['POST'])
@jwt_required()
def create_role():
    try:
        role_name = request.json.get('role_name', None)
        code = request.json.get('code', None)
        user = get_jwt_identity()

        if not role_name:
            return 'Role Name is Required', 400
        if not code:
            return 'Username is Required', 400
        if mongo.db.roles.find_one({'code': code}) is not None:
            return 'Code already exists', 400
        if mongo.db.roles.find_one({'role_name': role_name}) is not None:
            return 'Role already exists', 400

        _id = mongo.db.roles.insert({
            'role_name': role_name,
            'code': code,
            'created_at': datetime.utcnow(),
            'created_by': ObjectId(user["_id"])
        })

        return f'{role_name} is successfully created', 200

    except AttributeError:
        return 'Provide an Role Name and Code in JSON in request body', 400


@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username:
            return 'Username/Email/Phone is Required', 400

        if not password:
            return 'Password is Required', 400

        get_user1 = mongo.db.users.find_one({'username': username})
        get_user2 = mongo.db.users.find_one({'email': username})
        get_user3 = mongo.db.users.find_one({'phone': username})

        if (get_user1 is None) and (get_user2 is None) and (get_user3 is None):
            return 'User doesn\'t exists', 400

        get_user = {}
        if get_user1 is not None:
            get_user = get_user1

        if get_user2 is not None:
            get_user = get_user2

        if get_user3 is not None:
            get_user = get_user3

        if check_password_hash(pwhash=get_user['password'], password=password):
            access_token = create_access_token(identity={'_id': str(get_user["_id"]), 'role_id': str(get_user["role_id"])})
            refresh_token = create_refresh_token(identity={'_id': str(get_user["_id"]), 'role_id': str(get_user["role_id"])})
            return {'_id': str(get_user["_id"]), 'access_token': access_token, 'refresh_token': refresh_token}, 200

        return 'Invalid Password', 401

    except AttributeError:
        return 'Provide an Name, Username and Password in JSON in request body', 400


@app.route('/user/<id>', methods=['GET'])
@jwt_required()
def get_one_user(id):
    user = get_jwt_identity()
    print(user)
    users = mongo.db.users.find_one({'_id': ObjectId(id)})
    resp = dumps(users)
    return resp


@app.route('/user/delete/<id>', methods=['DELETE'])
def delete_one_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    resp = jsonify('user is successfully deleted')
    resp.status_code = 200
    return resp


@app.route('/users', methods=['GET'])
def get_all_users():
    users = mongo.db.users.find()
    resp = dumps(users)
    return resp


@app.route('/user/update/<id>', methods=['PUT'])
def update_one_user(id):
    _id = id
    if request.json['name'] and request.json['username'] and request.json['password'] and request.method == 'PUT':
        _hashed_password = generate_password_hash(request.json["password"])
        mongo.db.users.update_one({
            '_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)
        }, {
            '$set': {
                'name': request.json['name'],
                'username': request.json['username'],
                'password': _hashed_password
            }
        })
        resp = jsonify('user is successfully updated')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found ' + request.url
    }

    resp = jsonify(message)
    resp.status_code = 404

    return resp
