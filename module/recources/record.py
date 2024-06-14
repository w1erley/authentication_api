from flask import jsonify, request, Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from module.models import CategoryModel, RecordModel, db
from module.schemas import RecordSchema


record_blueprint = Blueprint('records', __name__, url_prefix="/records")
api = Api(record_blueprint)

class RecordList(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        
        records = (
            RecordModel.query
            .join(CategoryModel, RecordModel.category_id == CategoryModel.id)
            .filter(CategoryModel.user_id == None)  # Фільтр на категорії з user_id, що дорівнює None
            .all()
        )

        user_records = (
            RecordModel.query
            .join(CategoryModel, RecordModel.category_id == CategoryModel.id)
            .filter(CategoryModel.user_id == user_id)  # Фільтр на категорії з user_id, що дорівнює user_id
            .all()
        )
        serializer = RecordSchema(many=True)
        return {"records": serializer.dump(records), "user_records": serializer.dump(user_records)}
    
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        serializer = RecordSchema()
        validated_data = serializer.load(request.json)
        validated_data["user_id"] = user_id

        category = CategoryModel.query.get(validated_data["category_id"])
        if category:
            if category.user_id:
                if category.user_id != user_id:
                    return {"error": "You cant create record with category of an other user"}, 404
        else:
            return {"error": "No category with such id"}, 404
        
        record = RecordModel(**validated_data)
        db.session.add(record)
        db.session.commit()

        return {"msg": "Record created", "record": serializer.dump(record)}
    

class RecordResource(Resource):
    @jwt_required()
    def get(self, record_id):
        user_id = get_jwt_identity()

        record = (
            RecordModel.query
            .join(CategoryModel, RecordModel.category_id == CategoryModel.id)
            .filter(RecordModel.id == record_id)
            .filter(
                (CategoryModel.user_id == None) | (CategoryModel.user_id == user_id)
            )
            .first()
        )

        if record is None:
            return {"message": f"No record with such parameters found"}, 404
        serializer = RecordSchema()
        return {"record": serializer.dump(record)}
    
    @jwt_required()
    def delete(self, record_id):
        user_id = get_jwt_identity()

        record = (
            RecordModel.query
            .join(CategoryModel, RecordModel.category_id == CategoryModel.id)
            .filter(RecordModel.id == record_id)
            .filter(RecordModel.user_id == user_id)
            .first()
        )

        if not record:
            return {"error": "There is not a record with such parameters"}, 404

        db.session.delete(record)
        db.session.commit()

        return {"msg": "Record deleted"}


api.add_resource(RecordList, '/')
api.add_resource(RecordResource, '/<int:record_id>')