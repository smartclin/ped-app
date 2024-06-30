from flask import jsonify, request, current_app
import jwt
from functools import wraps
from app.models import User


# Utility function to handle JSON responses
def response_json(message, status=200):
    return jsonify({"message": message}), status


# Authentication decorator using JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            # Decode the token with expiration verification
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], verify_expiration=True
            )
            current_user = User.query.filter_by(id=data["id"]).first()
        except jwt.exceptions.DecodeError:
            return response_json("Invalid token format!", 401)
        except jwt.exceptions.ExpiredSignatureError:
            return response_json("Token has expired!", 401)
        except Exception as e:  # Catch other unexpected errors
            # Log the error for debugging
            print(f"An unexpected error occurred: {e}")
            return response_json("Internal server error", 500)

        return f(current_user, *args, **kwargs)  # Call the decorated function

    return decorated
