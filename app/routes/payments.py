from flask import Blueprint, request
from app import db
from app.models import Appointment
from app.utils import response_json, token_required

payments = Blueprint("payments", __name__)


# Make Payment for Appointment
@payments.route("/pay", methods=["POST"])
@token_required
def make_payment(current_user):
    data = request.get_json()

    if not data or not data.get("appointment_id") or not data.get("amount"):
        return response_json("Missing required fields", 400)

    appointment = Appointment.query.get(data["appointment_id"])

    if not appointment:
        return response_json("Appointment not found", 404)

    appointment.status = "Paid"
    db.session.commit()

    return response_json("Payment successful")


# Refund Payment for Appointment
@payments.route("/refund", methods=["POST"])
@token_required
def refund_payment(current_user):
    data = request.get_json()

    if not data or not data.get("appointment_id"):
        return response_json("Missing required fields", 400)

    appointment = Appointment.query.get(data["appointment_id"])

    if not appointment:
        return response_json("Appointment not found", 404)

    # Implement refund processing logic here

    appointment.status = "Refunded"
    db.session.commit()

    return response_json("Refund successful")
