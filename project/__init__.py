from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_restful import Api

app = Flask(__name__)

app.config["SECRET_KEY"] = "9c997a0adceb49999c65c61bb31936e9"
app.config["MONGO_URI"] = "mongodb://localhost:27017/flask-jwt"
app.config["JWT_SECRET_KEY"] = "51ec8b612fa34c5789f27b93813d4f96"

jwt = JWTManager(app)
api = Api(app)
mongo = PyMongo(app)

from project import routes