from flask import jsonify, request, Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from module.models import CategoryModel, db
from module.schemas import CategorySchema


category_blueprint = Blueprint('categories', __name__, url_prefix="/categories")
api = Api(category_blueprint)

class CategoryList(Resource):
    @jwt_required()
    def get(self):
        categories = CategoryModel.query.filter(CategoryModel.user_id == None).all()

        user_id = get_jwt_identity()

        user_categories = CategoryModel.query.filter(CategoryModel.user_id == user_id).all()
        serializer = CategorySchema(many=True)

        return {"categories": serializer.dump(categories), "user_categories": serializer.dump(user_categories)}
    
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        data = request.json
        data["creator_id"] = user_id

        serializer = CategorySchema()
        validated_data = serializer.load(data)

        category = CategoryModel(**validated_data)
        db.session.add(category)
        db.session.commit()

        return {"msg": "Category created", "category": serializer.dump(category)}
    

class CategoryResource(Resource):
    @jwt_required()
    def get(self, category_id):
        user_id = get_jwt_identity()

        category = CategoryModel.query.get(category_id)
        if category is None:
            return {"message": f"No category with id {category_id} found"}, 404
        
        if category.user_id and category.user_id != user_id:
            return {"message": "Not enough permissions"}, 404
        
        serializer = CategorySchema()
        return {"category": serializer.dump(category)}
    
    @jwt_required()
    def delete(self, category_id):
        user_id = get_jwt_identity()

        category = CategoryModel.query.filter(CategoryModel.creator_id == user_id , CategoryModel.id == category_id).first()  #DELETE ONLY URS
        if category is None:
            return {"message": f"No category with id {category_id} found"}, 404

        db.session.delete(category)
        db.session.commit()

        return {"msg": "Category deleted"}
    

class UserCategoryList(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        data = request.json
        data["user_id"] = user_id
        data["creator_id"] = user_id

        serializer = CategorySchema()
        validated_data = serializer.load(data)
        
        user_category = CategoryModel(**validated_data)
        db.session.add(user_category)
        db.session.commit()

        return {"msg": "User category created", "user_category": serializer.dump(user_category)}


api.add_resource(CategoryList, '/')
api.add_resource(CategoryResource, '/<int:category_id>')
api.add_resource(UserCategoryList, '/user')
