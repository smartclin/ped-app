from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from app import db
from app.models import User
from app.utils import response_json, token_required

auth = Blueprint("auth", __name__)


# User Registration
@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if (
        not data
        or not data.get("username")
        or not data.get("email")
        or not data.get("password")
    ):
        return response_json("Missing required fields", 400)

    hashed_password = generate_password_hash(data["password"], method="sha256")
    new_user = User(
        username=data["username"],
        email=data["email"],
        password=hashed_password,
        role="patient",
    )

    db.session.add(new_user)
    db.session.commit()

    return response_json("User registered successfully")


# User Login
@auth.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    app_config = current_app.config

    if not auth or not auth.username or not auth.password:
        return response_json("Invalid username or password", 401)

    user = User.query.filter_by(username=auth.username).first()

    if not user or not check_password_hash(user.password, auth.password):
        return response_json("Invalid username or password", 401)

    token = jwt.encode(
        {"id": user.id, "exp": datetime.utcnow() + timedelta(hours=24)},
        app_config["SECRET_KEY"],
        algorithm="HS256"
    )

    return jsonify({"token": token})


# Example Protected Route
@auth.route("/protected", methods=["GET"])
@token_required
def protected_route(current_user):
    message = f"Hello, {current_user.username}! This is a protected route."

    try:
        return response_json(message)  # Assuming response_json returns JSON
    except Exception as e:
        # Handle potential errors from response_json
        return jsonify({"error": str(e)}), 500  # Return error response
