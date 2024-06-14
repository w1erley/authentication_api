from flask import jsonify, request
from flask_restful import Resource
from passlib.hash import pbkdf2_sha256

from module.models import UserModel, db
from module.schemas import UserSchema


