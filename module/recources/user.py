from flask import jsonify, request, Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from module.models import UserModel, db
from module.schemas import UserSchema


user_blueprint = Blueprint('users', __name__, url_prefix="/users")
api = Api(user_blueprint)

class UserList(Resource):
    @jwt_required()
    def get(self):
        users = UserModel.query.all()
        serializer = UserSchema(many=True)
        return {"users": serializer.dump(users)}
    

class UserResource(Resource):
    @jwt_required()
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if user is None:
            return {"message": f"No user with id {user_id} found"}, 404

        serializer = UserSchema()
        return {"user": serializer.dump(user)}

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        if user is None:
            return {f"message": f"No user with id {user_id} found"}, 404
        
        if user.id != get_jwt_identity():
            return {f"message": "Not enough permissions"}, 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({"msg": "User deleted"})
    

api.add_resource(UserList, '/')
api.add_resource(UserResource, '/<int:user_id>')