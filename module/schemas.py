from marshmallow import Schema, fields, validates_schema, ValidationError
from .models import UserModel, CategoryModel


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class CategorySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    user_id = fields.Integer()
    creator_id = fields.Integer()

    @validates_schema
    def validate_unique_category_name(self, data, **kwargs):
        name = data.get('name')
        user_id = data.get('user_id')

        existing_category = CategoryModel.query.filter_by(name=name, user_id=user_id).first()
        if existing_category:
            raise ValidationError(f'Category with name {name} already exists for this user.')


class RecordSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    category_id = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)
    sum = fields.Float(required=True)