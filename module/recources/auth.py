from flask import jsonify, request, Blueprint
from flask_restful import Api, Resource
from passlib.hash import pbkdf2_sha256

from module.models import UserModel, db
from module.schemas import UserSchema


auth_blueprint = Blueprint('auth', __name__, url_prefix="/auth")
api = Api(auth_blueprint, errors=auth_blueprint.errorhandler)


class UserRegister(Resource):
    def post(self):
        data = request.json
        data["password"] = pbkdf2_sha256.hash(data["password"])

        serializer = UserSchema()
        validated_data = serializer.load(data)

        user = UserModel(**validated_data)
        db.session.add(user)
        db.session.commit()

        token = user.get_token()
        return {'access_token': token}
    

class UserLogin(Resource):
    def post(self):
        try:
            serializer = UserSchema()
            validated_data = serializer.load(request.json)

            user = UserModel.authenticate(**validated_data)

            token = user.get_token()
            return jsonify({'access_token': token})
        except Exception as e:
            return jsonify({'error': str(e)})
        

api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")