from datetime import datetime
from passlib.hash import pbkdf2_sha256

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from marshmallow import ValidationError

from .init_data import users, categories, records
from .models import db
from .models import UserModel, CategoryModel, RecordModel

from .recources.auth import auth_blueprint
from .recources.user import user_blueprint
from .recources.category import category_blueprint
from .recources.record import record_blueprint


app = Flask(__name__)
app.app_context().push()

app.config.from_pyfile('config.py', silent=True)

app.register_blueprint(auth_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(category_blueprint)
app.register_blueprint(record_blueprint)

@app.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400

@app.errorhandler(Exception)
def handle_error(error):
    response = jsonify({'error': str(error)})
    response.status_code = 500
    return response

db.init_app(app)

jwt = JWTManager(app)

migrate = Migrate(app, db)

db.create_all()

def initialize_users():
    tables = [UserModel, CategoryModel, RecordModel]
    
    if all(not table.query.first() for table in tables):
        for user_data in users:
            user_data["password"] = pbkdf2_sha256.hash(user_data["password"])
            user = UserModel(**user_data)
            db.session.add(user)
        
        for category_data in categories.values():
            category = CategoryModel(**category_data)
            db.session.add(category)
        
        for record_data in records.values():
            record_data["created_at"] = datetime.strptime(record_data["created_at"], "%Y-%m-%dT%H:%M:%S")
            record = RecordModel(**record_data)
            db.session.add(record)
        
        db.session.commit()
        print("Data added to the database.")
    else:
        print("Database is not empty, data was not added.")

initialize_users()