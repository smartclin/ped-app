from flask import Blueprint, jsonify, request
from app import db
from app.models import HealthTip
from app.utils import response_json, token_required

health_tips = Blueprint("health_tips", __name__)


# Get Health Tips
@health_tips.route("/tips", methods=["GET"])
def get_health_tips():
    tips = HealthTip.query.all()
    tips_data = [
        {"id": tip.id,
         "title": tip.title,
         "content": tip.content}
        for tip in tips]
    return jsonify(tips_data)


# Add Health Tip (Admin Only)
@health_tips.route("/tip", methods=["POST"])
@token_required  # Apply token_required decorator here
def add_health_tip(current_user):
    if current_user.role != "admin":
        return response_json("Unauthorized", 403)

    data = request.get_json()

    if not data or not data.get("title") or not data.get("content"):
        return response_json("Missing required fields", 400)

    new_tip = HealthTip(title=data["title"], content=data["content"])
    db.session.add(new_tip)
    db.session.commit()

    return response_json("Health tip added successfully")
