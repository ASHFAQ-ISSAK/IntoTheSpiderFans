from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserResource(Resource):
    def post(self):
        # Get the data from the request body
        data = request.get_json()

        # Extract the required properties
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"error": "User already exists"}, 400

        # Create a new User object
        user = User(username=username, email=email)
        user.set_password(password)

        # Add the object to the database session
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully"}, 201

    def get(self):
        users = User.query.all()
        data = [
            {"id": user.id, "username": user.username, "email": user.email}
            for user in users
        ]
        return data


class SingleUserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            data = {"id": user.id, "username": user.username, "email": user.email}
            return data
        else:
            return {"error": "User not found"}, 404

    def put(self, user_id):
        # Get the data from the request body
        data = request.get_json()

        # Check if the user exists
        user = User.query.get(user_id)
        if user:
            # Update the user details
            user.username = data.get("username", user.username)
            user.email = data.get("email", user.email)
            db.session.commit()
            return {"message": "User updated successfully"}
        else:
            return {"error": "User not found"}, 404

    def patch(self, user_id):
        # Get the data from the request body
        data = request.get_json()

        # Check if the user exists
        user = User.query.get(user_id)
        if user:
            # Update the user password if provided in the request data
            new_password = data.get("password")
        if new_password:
            user.update_password(new_password)

        # Update the user details selectively
        if "username" in data:
            user.username = data["username"]
        if "email" in data:
            user.email = data["email"]

            db.session.commit()
            return {"message": "User updated successfully"}
        else:
            return {"error": "User not found"}, 404

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted successfully"}
        else:
            return {"error": "User not found"}, 404


api.add_resource(UserResource, "/users")
api.add_resource(SingleUserResource, "/users/<int:user_id>")


if __name__ == "__main__":
    app.run(port=5555)
