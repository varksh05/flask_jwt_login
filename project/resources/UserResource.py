from datetime import datetime

from bson import ObjectId
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash

from project import mongo
from flask_jwt_extended import jwt_required, get_jwt_identity
