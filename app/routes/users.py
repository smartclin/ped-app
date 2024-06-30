from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from app.utils import response_json, token_required

users = Blueprint("users", __name__)


# Get All Users (Admin Only)
@users.route("/users", methods=["GET"])
@token_required
def get_all_users(current_user):
    if current_user.role != "admin":
        return response_json("Unauthorized", 403)

    users = User.query.all()
    users_data = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
        }
        for user in users
    ]
    return jsonify(users_data)


# Get User Profile
@users.route("/profile", methods=["GET"])
@token_required
def get_user_profile(current_user):
    user_data = {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
    }
    return jsonify(user_data)


# Update User Profile
@users.route("/profile", methods=["PUT"])
@token_required
def update_user_profile(current_user):
    data = request.get_json()

    if "username" in data:
        current_user.username = data["username"]
    if "email" in data:
        current_user.email = data["email"]

    db.session.commit()

    return response_json("User profile updated successfully")


# Delete User Account
@users.route("/profile", methods=["DELETE"])
@token_required
def delete_user_account(current_user):
    db.session.delete(current_user)
    db.session.commit()

    return response_json("User account deleted successfully")
